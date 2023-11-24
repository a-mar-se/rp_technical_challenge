from django.test import TestCase
from .validators import data_type_validator;

class ValidatorTestCase(TestCase):
# Create your tests here.
    def test_integer(self):
        values = ["1",'1.1','dfd','https://www.google.com']
        expected_result= [True,False,False,False]
        for va_index in range(len(values)):
            validation = data_type_validator(values[va_index], "integer")
            if (expected_result[va_index] == True):
                self.assertEqual(validation, True)
            else:
                self.assertNotEqual(validation, True)

    def test_decimal(self):
        values = ["1",'1.1','dfd','https://www.google.com']
        expected_result= [False,True,False,False]
        for va_index in range(len(values)):
            validation = data_type_validator(values[va_index], "decimal")
            if (expected_result[va_index] == True):
                self.assertEqual(validation, True)
            else:
                self.assertNotEqual(validation, True)

    def test_string(self):
        values = ["1",'1.1','dfd','https://www.google.com']
        expected_result= [True,True,True,True]
        for va_index in range(len(values)):
            validation = data_type_validator(values[va_index], "string")
            if (expected_result[va_index] == True):
                self.assertEqual(validation, True)
            else:
                self.assertNotEqual(validation, True)
    
    def test_url(self):
        values = ["1",'1.1','dfd','https://www.google.com']
        expected_result= [False,False,False,True]
        for va_index in range(len(values)):
            validation = data_type_validator(values[va_index], "url")
            if (expected_result[va_index] == True):
                self.assertEqual(validation, True)
            else:
                self.assertNotEqual(validation, True)

    def test_favicon(self):
        values = ["1",'1.1','dfd','https://www.google.com']
        expected_result= [False,False,False,True]
        for va_index in range(len(values)):
            validation = data_type_validator(values[va_index], "favicon")
            if (expected_result[va_index] == True):
                self.assertEqual(validation, True)
            else:
                self.assertNotEqual(validation, True)