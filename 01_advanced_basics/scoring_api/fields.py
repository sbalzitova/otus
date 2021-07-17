import re
import datetime
import logging


logging.basicConfig(filename='script_log.txt',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%Y.%m.%d %H:%M:%S',
                    level=logging.INFO)


class Field:
    def __init__(self, value=None, required=False, nullable=True):
        self.required = required
        self.nullable = nullable
        self.value = value

    def is_valid(self, *args):
        pass

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        logging.debug('Using descriptor __set__ method')
        if value is None and (self.required or self.nullable):
            raise ValueError('{} cannot be null'.format(self.__class__.__name__))
        elif self.is_valid(value):
            self.value = value
        else:
            raise ValueError('{} has invalid value'.format(self.__class__.__name__))

    def __add__(self, other):
        return self.value + other.value


class CharField(Field):
    def __init__(self, required=False, nullable=False):
        super(CharField, self).__init__(required, nullable)

    def is_valid(self, value):
        logging.debug('CharField validation goes on')
        if isinstance(value, str):
            return True
        return False


class ArgumentsField(Field):
    def __init__(self, required=False, nullable=False):
        super(ArgumentsField, self).__init__(required, nullable)

    def is_valid(self, value):
        logging.debug('ArgumentsField validation goes on')
        if isinstance(value, dict):
            return True
        return False


class EmailField(CharField):
    def __init__(self, required=False, nullable=False):
        super(EmailField, self).__init__(required, nullable)

    def is_valid(self, value):
        logging.debug('EmailField validation goes on')
        is_email = re.match(r'[\w]+@[\w]+', value)
        if is_email:
            return True
        return False


class PhoneField(Field):
    def __init__(self, required=False, nullable=False):
        super(PhoneField, self).__init__(required, nullable)

    def is_valid(self, value):
        logging.debug('PhoneField validation goes on')
        is_phone = re.match(r'7\d{10}', str(value))
        if is_phone:
            return True
        return False


class DateField(Field):
    def __init__(self, required=False, nullable=False):
        super(DateField, self).__init__(required, nullable)

    def is_valid(self, value):
        is_date = re.match(r'(?P<date>\d{6,8})', str(value))
        if is_date:
            return True
        return False


class BirthDayField(Field):
    def __init__(self, required=False, nullable=False):
        super(BirthDayField, self).__init__(required, nullable)

    def is_valid(self, value):
        try:
            value_to_date = datetime.datetime.strptime(value, "%d.%m.%Y").date()
            now = datetime.datetime.now().date()
            if now - value_to_date < datetime.timedelta(25567):  # 70 years
                return True
        except ValueError:
            return False

        return False


class GenderField(Field):
    def __init__(self, required=False, nullable=False):
        super(GenderField, self).__init__(required, nullable)

    def is_valid(self, value):
        if not isinstance(value, int):
            return False

        is_gender = re.match(r'[012]', str(value))
        if is_gender:
            return True
        return False


class ClientIDsField(Field):
    def __init__(self, required=False, nullable=False):
        super(ClientIDsField, self).__init__(required, nullable)

    def is_valid(self, value):
        if isinstance(value, int):
            return True
        return False
