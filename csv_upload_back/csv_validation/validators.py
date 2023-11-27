from django.core.exceptions import ValidationError
from django.core.validators import URLValidator, DecimalValidator, RegexValidator
from django.forms import DecimalField, IntegerField
import math


def validate_extra(regex_value, value, message, test_value):
    print("validatin extra")
    try:
        val = RegexValidator(regex_value, message + test_value , "")
        re = val(value)
        return re
    except ValidationError as e:
        print(e)
        return e
    
def data_type_validator(value, data_type, table_extra_validations = None):
    if type(value) == "number":
        if math.isnan(value):
            return "value is empty"
        
    if len(str(value)) == 0:
        return "value is empty"
    
    if 'basic_data_type' in table_extra_validations.keys():
        data_type = table_extra_validations["basic_data_type"]

    if 'extra' in table_extra_validations.keys():
        if (table_extra_validations["extra"] != None):
            if data_type == "decimal":
                if (table_extra_validations["extra"]["decimal_point"] != None):
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
                    if table_extra_validations["extra"]["n_decimals"] == '.':
                        val =validate_extra("^\d*\.\d{" + str(table_extra_validations["extra"]["n_decimals"]) + "}$", str(value), "value doesn't have correct number of decimals ", table_extra_validations["extra"]["n_decimals"])
                        if (val != None):
                            return val
                    elif table_extra_validations["extra"]["n_decimals"] == ',':
                        val =validate_extra("^\d*\,\d{" + str(table_extra_validations["extra"]["n_decimals"]) + "}$", str(value), "value doesn't have correct number of decimals ", table_extra_validations["extra"]["n_decimals"])
                        if (val != None):
                            return val
            
            if (table_extra_validations["extra"]["max_length"] != None):
                
                val = validate_extra("^.{1," + table_extra_validations["extra"]["max_length"] + "}$",str(value), "value is longer than ", table_extra_validations["extra"]["max_length"] )
                if (val != None):
                    return val

            if (table_extra_validations["extra"]["starting_with"] != None):
                val = validate_extra("^"+table_extra_validations["extra"]["starting_with"],value, "value doesn't start with ", table_extra_validations["extra"]["starting_with"])
                if (val != None):
                    return val
                
            if (table_extra_validations["extra"]["ending_with"] != None):
                val = validate_extra(""+table_extra_validations["extra"]["ending_with"] + "$", value, "value doesn't end with ", table_extra_validations["extra"]["ending_with"])
                if (val != None):
                    return val
            
            if (table_extra_validations["extra"]["contains"] != None):
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
            reg = '^[-+]?\d+$'
            try:
                val = RegexValidator(reg, "please provide an integer number", "Wrong integer format")
                re = val(value)
                return True
            except ValidationError as e:
                print(e)
                return e
        case "string":
            reg = "\w"
            try:
                val = RegexValidator(reg, "please provide a decimal number", "Wrong decimal format")
                re = val(value)
                return True
            except ValidationError as e:
                return e
        case "url":
            try:
                vaa = URLValidator(message = "Please provide a valid url")
                vaa(value)
                return True
            except ValidationError as exception:
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