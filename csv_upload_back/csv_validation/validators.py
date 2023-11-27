from django.core.exceptions import ValidationError
from django.core.validators import URLValidator, DecimalValidator, RegexValidator
from django.forms import DecimalField, IntegerField
import math


def validate_extra(regex_value, value, message, test_value):
    try:
        val = RegexValidator(regex_value, message + test_value , "")
        re = val(value)
        return re
    except ValidationError as e:
        print(e)
        return e
    
def data_type_validator(value, data_type, table_extra_validations = None):
    print(table_extra_validations)
    print(value)
    if type(value) == "number":
    
        if math.isnan(value):
            return "value is empty"
    if len(str(value)) == 0:
        return "value is empty"
    
    print("__________dfsdfsf__________________")
    print(table_extra_validations)
    # if (table_extra_validations["basic_data_type"] != None):
    if hasattr(table_extra_validations, 'basic_data_type'):
        data_type = table_extra_validations["basic_data_type"]

    if hasattr(table_extra_validations, 'extra'):
    # if (table_extra_validations["extra"] != None):
        if data_type == "decimal":
            if (table_extra_validations["extra"]["decimal_point"] != None):
                print("ther eis decimal_point")
                if table_extra_validations["extra"]["decimal_point"] == '.':
                    val = validate_extra("^.*\\" + str(table_extra_validations["extra"]["decimal_point"]) + ".*$", str(value), "decimal point not found ", table_extra_validations["extra"]["decimal_point"])
                    if (val != None):
                        return val
                elif table_extra_validations["extra"]["decimal_point"] == ',':
                    val = validate_extra("^.*\\" + str(table_extra_validations["extra"]["decimal_point"]) + ".*$", str(value), "decimal point not found ", table_extra_validations["extra"]["decimal_point"])
                    if (val != None):
                        return val
                    value = str(value).replace(",",".")
                
            if (table_extra_validations["extra"]["n_decimals"] != None):
                print("ther eis n_decimals")
                if table_extra_validations["extra"]["n_decimals"] == '.':
                    val =validate_extra("^\d*\.\d{" + str(table_extra_validations["extra"]["n_decimals"]) + "}$", str(value), "value doesn't have correct number of decimals ", table_extra_validations["extra"]["n_decimals"])
                    if (val != None):
                        return val
                elif table_extra_validations["extra"]["n_decimals"] == ',':
                    val =validate_extra("^\d*\,\d{" + str(table_extra_validations["extra"]["n_decimals"]) + "}$", str(value), "value doesn't have correct number of decimals ", table_extra_validations["extra"]["n_decimals"])
                    if (val != None):
                        return val
        
        print(value)
        if (table_extra_validations["extra"]["max_length"] != None):
            print("ther eis max_len")
            val = validate_extra("^.{1," + table_extra_validations["extra"]["max_length"] + "}$",str(value), "value is longer than ", table_extra_validations["extra"]["max_length"] )
            if (val != None):
                return val



        if (table_extra_validations["extra"]["starting_with"] != None):
            print("ther eis starting_with")
            val = validate_extra("^"+table_extra_validations["extra"]["starting_with"],value, "value doesn't start with ", table_extra_validations["extra"]["starting_with"])
            if (val != None):
                return val
        if (table_extra_validations["extra"]["ending_with"] != None):
            print("ther eis ending")
            val = validate_extra(""+table_extra_validations["extra"]["ending_with"] + "$", value, "value doesn't end with ", table_extra_validations["extra"]["ending_with"])
            if (val != None):
                return val
        
        if (table_extra_validations["extra"]["contains"] != None):
            print("ther eis contain")
            val =validate_extra("^.*" + str(table_extra_validations["extra"]["contains"]) + ".*$", str(value), "value doesn't contain ", table_extra_validations["extra"]["contains"])
            if (val != None):
                return val
            
        
            
    match data_type:
        case "decimal":
            reg = "\d\.\d"
            try:
                val = RegexValidator(reg, "please provide a decimal number", "Wrong decimal format")
                re = val(value)
                return True
            except ValidationError as e:
                print(e)
                return e
        case "integer":
            print('integer')
            # reg = 'r"[+-]?(?<!\.)\b[0-9]+\b(?!\.[0-9])"'
            reg = '^[-+]?\d+$'
            try:
                # f = IntegerField(max_value=10^8 - 1)
                # print(f)
                # re = f(value)
                # print(re)
                val = RegexValidator(reg, "please provide an integer number", "Wrong integer format")
                re = val(value)
                print("validation error on integer. Right")
                print(re)
                return True
            except ValidationError as e:
                print("validation error on integer. Wrong")
                print(e)
                return e
        case "string":
            # decimal_regex()
            print('string')
            reg = "\w"
            try:
                val = RegexValidator(reg, "please provide a decimal number", "Wrong decimal format")
                re = val(value)
                print(re)
                return True
            except ValidationError as e:
                print(e)
                return e
        case "favicon":
            # decimal_regex()
            print('favicon')
            try:
                vaa = URLValidator(message = "Please provide a valid url")
                vaa(value)
                return True
            except ValidationError as exception:
                # URL is NOT valid here.
                # handle exception..
                print(exception)
                return exception

            # try:
            #     val = RegexValidator(reg, "please provide a decimal number", "Wrong decimal format")
            #     re = val(value)
            #     print(re)
            # except ValidationError as e:
            #     print(e)
            #     return e
            # valid_url(value)
        case "url":
            # decimal_regex()
            print('url')
            try:
                vaa = URLValidator(message = "Please provide a valid url")
                vaa(value)
                # URLValidator(value,"Please provide a valid url")
                # url is valid here
                # do something, such as:
                return True
            except ValidationError as exception:
                # URL is NOT valid here.
                # handle exception..
                print("ValidationError exception")
                print(exception)
                return exception


def valid_url(value:str) -> bool:
    # validator = URLValidator()
    try:
        URLValidator(value)
        # url is valid here
        # do something, such as:
        return True
    except ValidationError as exception:
        # URL is NOT valid here.
        # handle exception..
        print(exception)
        return False
    
def valid_decimal(value:str, decimal_places = None) -> bool:
    # validator = URLValidator()
    try:
        if (decimal_places != None):
            DecimalValidator(value, decimal_places=decimal_places)
        else:
            DecimalValidator(value)
        # url is valid here
        # do something, such as:
        return True
    except ValidationError as exception:
        # URL is NOT valid here.
        # handle exception..
        print(exception)
        return False
    
def regex_validator(reg,  message, code):
    return RegexValidator(regex = reg, message= message, code=code)