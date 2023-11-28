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

    def test_starting_with(self):
        values = ["12",'12.1','12dfd','12https://www.google.com',"2",'2.1','1dfd','2https://www.google.com']
        expected_result= [True,True,True,True, False, False, False, False]
        for va_index in range(len(values)):
            validation = data_type_validator(values[va_index], "favicon",{'starting_with': '12'})
            if (expected_result[va_index] == True):
                self.assertEqual(validation == None, True)
            else:
                self.assertNotEqual(validation, True)

    def test_ending_with(self):
        values = ["12",'112.12','1dfd12','12https://www.google.com12',"2",'2.1','1dfd','2https://www.google.com']
        expected_result= [True,True,True,True, False, False, False, False]
        for va_index in range(len(values)):
            validation = data_type_validator(values[va_index], "favicon",{'ending_with': '12'})
            if (expected_result[va_index] == True):
                self.assertEqual(validation == None, True)
            else:
                self.assertNotEqual(validation, True)

    def test_contains(self):
        values = ["12",'12.132','12dfd132','12https://www.google.com132',"22312",'2.12','1dfd12','2https://www.google.com12',"221231",'2.121','1df12d1','2ht12tps://www.google.com1',"22131",'2.21','1df1d1','2ht1tps://www.google.com1']
        expected_result= [True,True,True,True,True,True,True,True,True,True,True,True, False, False, False, False]
        for va_index in range(len(values)):
            validation = data_type_validator(values[va_index], "favicon",{'contains': '12'})
            if (expected_result[va_index] == True):
                self.assertEqual(validation == None, True)
            else:
                self.assertNotEqual(validation, True)

    def test_max_length(self):
        values = ["1",'.','d',"22312",'2.12','1dfd12']
        expected_result= [True,True,True, False, False, False]
        for va_index in range(len(values)):
            validation = data_type_validator(values[va_index], "favicon",{'max_length': '1'})
            if (expected_result[va_index] == True):
                self.assertEqual(validation == None, True)
            else:
                self.assertNotEqual(validation, True)