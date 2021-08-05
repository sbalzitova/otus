import abc
import json
import datetime
import logging
import hashlib
import uuid
from .fields import Field, CharField, EmailField, PhoneField, BirthDayField, DateField, ArgumentsField, \
    ClientIDsField, GenderField, FieldValueError
from .scoring import get_score, get_interests
from optparse import OptionParser
from http.server import HTTPServer, BaseHTTPRequestHandler
from .store import Store


logging.basicConfig(filename='script_log.txt',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%Y.%m.%d %H:%M:%S',
                    level=logging.INFO)


SALT = "Otus"
ADMIN_LOGIN = "admin"
ADMIN_SALT = "42"
OK = 200
BAD_REQUEST = 400
FORBIDDEN = 403
NOT_FOUND = 404
INVALID_REQUEST = 422
INTERNAL_ERROR = 500
ERRORS = {
    BAD_REQUEST: "Bad Request",
    FORBIDDEN: "Forbidden",
    NOT_FOUND: "Not Found",
    INVALID_REQUEST: "Invalid Request",
    INTERNAL_ERROR: "Internal Server Error",
}
UNKNOWN = 0
MALE = 1
FEMALE = 2
GENDERS = {
    UNKNOWN: "unknown",
    MALE: "male",
    FEMALE: "female",
}


class RequestParser:
    def __init__(self, **kwargs):
        self.fields = {}
        self.values = kwargs
        self.has = {}

        for k, v in self.__class__.__dict__.items():
            if isinstance(v, Field):
                self.fields[k] = v

        for key, value in self.fields.items():
            self.fields[key].value = None
            if key in self.values.keys():
                setattr(self, key, self.values[key])


class ClientsInterestsRequest(RequestParser):
    client_ids = ClientIDsField(required=True)
    date = DateField(required=False, nullable=True)


class OnlineScoreRequest(RequestParser):
    first_name = CharField(required=False, nullable=True)
    last_name = CharField(required=False, nullable=True)
    email = EmailField(required=False, nullable=True)
    phone = PhoneField(required=False, nullable=True)
    birthday = BirthDayField(required=False, nullable=True)
    gender = GenderField(required=False, nullable=True)


class MethodRequest(RequestParser):
    account = CharField(required=False, nullable=True)
    login = CharField(required=True, nullable=True)
    token = CharField(required=True, nullable=True)
    arguments = ArgumentsField(required=True, nullable=True)
    method = CharField(required=True, nullable=False)

    @property
    def is_admin(self):
        return self.login == ADMIN_LOGIN


def check_required_fields(obj, ctx):
    combinations = {'phone': 'email',
                    'first_name': 'last_name',
                    'gender': 'birthday',
                    'email': 'phone',
                    'last_name': 'first_name',
                    'birthday': 'gender'}

    if_required_fields_present = False

    for field, field_class in obj.fields.items():

        if field_class.value or field_class.value == 0:
            if combinations.get(field) in obj.has.keys() or field == 'client_ids':
                if_required_fields_present = True
            obj.has[field] = field_class.value

    ctx.update({'has': obj.has})

    return if_required_fields_present


def check_auth(request):
    if request.login == ADMIN_LOGIN:
        digest = hashlib.sha512((datetime.datetime.now().strftime("%Y%m%d%H") + ADMIN_SALT).encode()).hexdigest()
    else:
        digest = hashlib.sha512((request.account + request.login + SALT).encode()).hexdigest()
    if digest == request.token:
        return True
    return False


def calc_online_score(f, store, ctx):
    fields = OnlineScoreRequest(**f)
    return {"score": get_score(store, fields.phone, fields.email, fields.birthday, fields.gender, fields.first_name, fields.last_name)}


def calc_clients_interests(fields, store, ctx):
    res = {}
    clients = fields.get('client_ids')
    ctx.update({'nclients': len(clients)})
    for client in clients:
        res[client] = get_interests(store, client)
    return res


def method_handler(request, ctx, store):
    response, code = None, None

    try:
        logging.info('Parsing request')
        modeled_request = MethodRequest(**request['body'])
        method = modeled_request.method
        login = modeled_request.login
        arguments = modeled_request.arguments or {}

        logging.info('Parsing arguments')
        online_score_arguments = OnlineScoreRequest(**arguments)
        client_interest_arguments = ClientsInterestsRequest(**arguments)

        methods = {'online_score': (calc_online_score, online_score_arguments),
                   'clients_interests': (calc_clients_interests, client_interest_arguments)}

        if not modeled_request.values or not login or method not in methods.keys():
            code = INVALID_REQUEST
            response = ERRORS.get(code)
            logging.info('Request is invalid or empty, check method or login')
            return response, code

        if not check_auth(modeled_request):
            code = FORBIDDEN
            response = ERRORS.get(code)
            logging.info('Authorization failed')
            return response, code

        is_required_fields_present = check_required_fields(methods[method][1], ctx)
        if not is_required_fields_present:
            code = INVALID_REQUEST
            response = ERRORS.get(code)
            logging.info('Request does not have required fields')
            return response, code

        if login == 'admin':
            code = 200
            response = {"score": 42}
            logging.info('It is fun to be an admin')
            return response, code

        response = methods[method][0](ctx.get('has'), store, ctx)
        code = OK
        logging.info('Scoring is successfully done')

    except FieldValueError as e:
        code = INVALID_REQUEST
        response = str(e)
        logging.exception('Validation error')

    return response, code


class MainHTTPHandler(BaseHTTPRequestHandler):
    router = {
        "method": method_handler
    }
    store = Store()

    def get_request_id(self, headers):
        return headers.get('HTTP_X_REQUEST_ID', uuid.uuid4().hex)

    def do_POST(self):
        response, code = {}, OK
        context = {"request_id": self.get_request_id(self.headers)}
        request = None
        try:
            data_string = self.rfile.read(int(self.headers['Content-Length']))
            request = json.loads(data_string)
        except:
            code = BAD_REQUEST

        if request:
            path = self.path.strip("/")
            logging.info("%s: %s %s" % (self.path, data_string, context["request_id"]))
            if path in self.router:
                try:
                    response, code = self.router[path]({"body": request, "headers": self.headers}, context, self.store)
                except Exception as e:
                    logging.exception("Unexpected error: %s" % e)
                    code = INTERNAL_ERROR
            else:
                code = NOT_FOUND

        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        if code not in ERRORS:
            r = {"response": response, "code": code}
        else:
            r = {"error": response or ERRORS.get(code, "Unknown Error"), "code": code}
        context.update(r)
        logging.info(context)
        self.wfile.write(json.dumps(r))
        return


if __name__ == "__main__":
    op = OptionParser()
    op.add_option("-p", "--port", action="store", type=int, default=8080)
    op.add_option("-l", "--log", action="store", default=None)
    (opts, args) = op.parse_args()
    logging.basicConfig(filename=opts.statistics, level=logging.INFO,
                        format='[%(asctime)s] %(levelname).1s %(message)s', datefmt='%Y.%m.%d %H:%M:%S')
    server = HTTPServer(("localhost", opts.port), MainHTTPHandler)
    logging.info("Starting server at %s" % opts.port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
