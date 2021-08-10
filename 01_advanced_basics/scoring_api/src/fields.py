import re
import datetime
import logging


class FieldValueError(BaseException):
    pass


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
        logging.debug('Using descriptor __set__ method')
        if value is None and (self.required or self.nullable):
            raise FieldValueError('{} cannot be null'.format(self.__class__.__name__))
        elif self.is_valid(value):
            field = None
            for k, v in instance.values.items():
                if v == value:
                    field = k
            instance.fields[field].value = value
        else:
            raise FieldValueError('Incorrect value {} of type {} was about to set to {}. Reason: {}'.format(
                value, type(value), self.__class__.__name__, self.validation_rule))


class CharField(Field):
    validation_rule = 'must be a string'

    def is_valid(self, value):
        return isinstance(value, str)


class ArgumentsField(Field):
    validation_rule = 'must be a json object'

    def is_valid(self, value):
        return isinstance(value, dict)


class EmailField(CharField):
    validation_rule = 'must contain @ symbol'

    def is_valid(self, value):
        is_email = re.match(r'[\w]+@[\w]+', value)
        if is_email:
            return True
        return False


class PhoneField(Field):
    validation_rule = 'must start with 7 and contain 11 digits'

    def is_valid(self, value):
        is_phone = re.match(r'7\d{10}', str(value))
        if is_phone:
            return True
        return False


class DateField(Field):
    validation_rule = 'must be date with DD.MM.YYYY format'

    def is_valid(self, value):
        try:
            datetime.datetime.strptime(value, "%d.%m.%Y").date()
            return True
        except ValueError:
            return False


class BirthDayField(DateField):
    def __init__(self, required=False, nullable=False):
        super(BirthDayField, self).__init__(required, nullable)
        self.validation_rule += ' and not more than 70 years ago'
        self.today = datetime.datetime.now().date()
        self.seventy_years = datetime.timedelta(25567)

    def is_valid(self, value):
        try:
            value_to_date = datetime.datetime.strptime(value, "%d.%m.%Y").date()
            return self.today - value_to_date < self.seventy_years
        except ValueError:
            return False


class GenderField(Field):
    validation_rule = 'must be an integer of 0 (man), 1 (woman) or 2 (unknown)'

    def is_valid(self, value):
        if not isinstance(value, int):
            return False

        is_gender = re.match(r'[012]', str(value))
        return bool(is_gender)


class ClientIDsField(Field):
    validation_rule = 'must be a non-empty array of integers'

    def is_valid(self, value):
        return isinstance(value, list) and set([isinstance(v, int) for v in value]) == {True}
