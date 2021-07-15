import abc
import json
import datetime
import logging
import hashlib
import uuid
from fields import *
from optparse import OptionParser
from http.server import HTTPServer, BaseHTTPRequestHandler

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


class ClientsInterestsRequest:
    client_ids = ClientIDsField(required=True)
    date = DateField(required=False, nullable=True)


class OnlineScoreRequest:
    def __init__(self, **kwargs):
        self.fields = {}
        self.values = kwargs

        for k, v in self.__class__.__dict__.items():
            if isinstance(v, Field):
                self.fields[k] = v

        for k, v in self.values.items():
            if k in self.fields.keys():
                self.fields[k].value = v

    def __get__(self, instance, owner):
        return self.values

    def if_required_fields_present(self):
        combinations = {'phone': 'email',
                        'first_name': 'last_name',
                        'gender': 'birthday',
                        'email': 'phone',
                        'last_name': 'first_name',
                        'birthday': 'gender'}

        found_combinations = []

        for field, field_class in self.fields.items():

            if field_class.value:
                if combinations.get(field) in found_combinations:
                    return True
                else:
                    found_combinations.append(field)
        return False

    first_name = CharField(required=False, nullable=True)
    last_name = CharField(required=False, nullable=True)
    email = EmailField(required=False, nullable=True)
    phone = PhoneField(required=False, nullable=True)
    birthday = BirthDayField(required=False, nullable=True)
    gender = GenderField(required=False, nullable=True)


class MethodRequest:
    def __init__(self, **kwargs):
        self.fields = self.__class__.__dict__
        self.values = kwargs['body']

        for k, v in self.values.items():
            if k in self.fields:
                self.fields[k].value = self.values[k]

    def __get__(self, instance, item):
        return self.values.get(item)

    account = CharField(required=False, nullable=True)
    login = CharField(required=True, nullable=True)
    token = CharField(required=True, nullable=True)
    arguments = ArgumentsField(required=True, nullable=True)
    method = CharField(required=True, nullable=False)

    @property
    def is_admin(self):
        return self.login == ADMIN_LOGIN


def check_auth(request):
    if request.login == ADMIN_LOGIN:
        digest = hashlib.sha512((datetime.datetime.now().strftime("%Y%m%d%H") + ADMIN_SALT).encode()).hexdigest()
    else:
        digest = hashlib.sha512((request.account + request.login + SALT).encode()).hexdigest()
    if digest == request.token:
        return True
    return False


def method_handler(request, ctx, store):
    response, code = None, None

    try:

        modeled_request = MethodRequest(**request)
        method = modeled_request.values.get('method')
        login = modeled_request.values.get('login')
        arguments = modeled_request.values.get('arguments') or {}

        modeled_arguments = OnlineScoreRequest(**arguments)

        if not modeled_request.values or not login or method != 'online_score':
            code = INVALID_REQUEST

        else:
            if not check_auth(modeled_request):
                code = FORBIDDEN

            else:
                is_required_fields_present = modeled_arguments.if_required_fields_present()
                if not is_required_fields_present:
                    code = INVALID_REQUEST

                else:
                    code = OK

    except ValueError:
        code = INVALID_REQUEST

    response = ERRORS.get(code)

    return response, code


class MainHTTPHandler(BaseHTTPRequestHandler):
    router = {
        "method": method_handler
    }
    store = None

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
