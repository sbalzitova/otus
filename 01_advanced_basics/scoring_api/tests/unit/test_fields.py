import unittest
from src.fields import CharField, EmailField, PhoneField, BirthDayField, DateField, ArgumentsField, ClientIDsField, \
    GenderField, FieldValueError
from src.api import Request


class Validation(unittest.TestCase):
    def template(self, class_field, val, res):
        req = Request()
        req.field = class_field()
        req.values['test_field'] = val
        req.fields['test_field'] = class_field()
        try:
            req.field.__set__(req, val)
        except FieldValueError:
            pass
        key = req.fields['test_field'].value
        self.assertEqual(key, res)


class TestCharFieldValidation(Validation):

    def test_value_valid(self):
        cases = [
            (CharField, 'valid_string', 'valid_string'),
            (CharField, """
            long
            string""", """
            long
            string"""),
            (CharField, '12345', '12345'),
            (CharField, '', ''),
        ]

        for case in cases:
            with self.subTest(case=case):
                self.template(*case)

    def test_value_invalid(self):
        cases = [
            (CharField, 123, None),
            (CharField, {'k': 'v'}, None),
            (CharField, ('o', 'oO'), None),

        ]
        for case in cases:
            with self.subTest(case=case):
                self.template(*case)


class TestArgumentsFieldValidation(Validation):

    def test_value_valid(self):
        cases = [
            (ArgumentsField, {'key': 'value'}, {'key': 'value'}),
            (ArgumentsField, {'key': 'value', 'key1': 'value1'}, {'key': 'value', 'key1': 'value1'}),
            (ArgumentsField, {}, {}),
        ]

        for case in cases:
            with self.subTest(case=case):
                self.template(*case)

    def test_value_invalid(self):
        cases = [
            (ArgumentsField, ('key', 'value'), None),
            (ArgumentsField, {'key', 'value'}, None),
        ]
        for case in cases:
            with self.subTest(case=case):
                self.template(*case)


class TestEmailFieldValidation(Validation):

    def test_value_valid(self):
        cases = [
            (EmailField, 'test@test.ru', 'test@test.ru'),
            (EmailField, 'test@test', 'test@test'),
            (EmailField, '123@test.ru', '123@test.ru'),
            (EmailField, 'o@o', 'o@o'),
        ]

        for case in cases:
            with self.subTest(case=case):
                self.template(*case)

    def test_value_invalid(self):
        cases = [
            (EmailField, 'testtest.ru', None),
            (EmailField, '', None),
            (EmailField, '12345', None),
            (EmailField, '@', None),
        ]
        for case in cases:
            with self.subTest(case=case):
                self.template(*case)


class TestPhoneFieldValidation(Validation):

    def test_value_valid(self):
        cases = [
            (PhoneField, 79999999900, 79999999900),
            (PhoneField, '79999999900', '79999999900'),
        ]

        for case in cases:
            with self.subTest(case=case):
                self.template(*case)

    def test_value_invalid(self):
        cases = [
            (PhoneField, 89999999900, None),
            (PhoneField, '99999999', None),
            (PhoneField, '999999999999999999999', None),
        ]
        for case in cases:
            with self.subTest(case=case):
                self.template(*case)


class TestBirthDayFieldValidation(Validation):

    def test_value_valid(self):
        cases = [
            (BirthDayField, '01.01.2010', '01.01.2010'),
            (BirthDayField, '12.12.2012', '12.12.2012'),
            (BirthDayField, '12.09.1961', '12.09.1961'),
        ]

        for case in cases:
            with self.subTest(case=case):
                self.template(*case)

    def test_value_invalid(self):
        cases = [
            (BirthDayField, '01.01.1910', None),
            (BirthDayField, '12.07.1940', None),
            (BirthDayField, '07.1940', None),
        ]
        for case in cases:
            with self.subTest(case=case):
                self.template(*case)


class TestDateFieldValidation(Validation):

    def test_value_valid(self):
        cases = [
            (DateField, '12.12.2012', '12.12.2012'),
            (DateField, '01.01.1001', '01.01.1001'),
        ]

        for case in cases:
            with self.subTest(case=case):
                self.template(*case)

    def test_value_invalid(self):
        cases = [
            (DateField, '32.32.2012', None),
            (DateField, '01.1001', None),
        ]
        for case in cases:
            with self.subTest(case=case):
                self.template(*case)


class TestGenderFieldValidation(Validation):

    def test_value_valid(self):
        cases = [
            (GenderField, 0, 0),
            (GenderField, 1, 1),
            (GenderField, 2, 2),
        ]

        for case in cases:
            with self.subTest(case=case):
                self.template(*case)

    def test_value_invalid(self):
        cases = [
            (GenderField, 9, None),
        ]
        for case in cases:
            with self.subTest(case=case):
                self.template(*case)

