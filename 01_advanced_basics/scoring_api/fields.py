import re
import datetime


class Field:
    def __init__(self, required=False, nullable=True):
        self.required = required
        self.nullable = nullable
        self.value = None

    def is_valid(self, *args):
        pass

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        if self.is_valid(value):
            print('im used')
            setattr(instance, self.value, value)
        else:
            raise ValueError('{} has invalid value'.format(self.__class__.__name__))

    def __add__(self, other):
        return self.value + other.value


class CharField(Field):
    def is_valid(self, value):
        if isinstance(value, str):
            return True
        return False


class ArgumentsField(Field):
    def is_valid(self, value):
        if isinstance(value, dict):
            return True
        return False


class EmailField(CharField):
    def is_valid(self, value):
        is_email = re.match(r'[\w]+@[\w]+', value)
        if is_email:
            return True
        return False


class PhoneField(Field):
    def is_valid(self, value):
        is_phone = re.match(r'7[+]?\d{10}', str(value))
        if is_phone:
            return True
        return False


class DateField(Field):
    def is_valid(self, value):
        is_date = re.match(r'(?P<date>\d{6,8})', str(value))
        if is_date:
            return True
        return False


class BirthDayField(Field):
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
    def is_valid(self, value):
        if not isinstance(value, int):
            return False

        is_gender = re.match(r'[012]', str(value))
        if is_gender:
            return True
        return False


class ClientIDsField(Field):
    def is_valid(self, value):
        if isinstance(value, int):
            return True
        return False
