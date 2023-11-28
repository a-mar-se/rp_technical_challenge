from django.core.exceptions import ValidationError
from django.core.validators import URLValidator, DecimalValidator, RegexValidator
import math



    
def data_type_validator(value, data_type, table_extra_validations = None):
    # Return error if the value is a number NaN
    if type(value) == "number":
        if math.isnan(value):
            return "value is empty"
        
    # Return error if value is empty
    if len(str(value)) == 0:
        return "value is empty"
    
    # Check if the provided data_type is a custom one
    if table_extra_validations != None:
        # Define the basic_data_type of the custom_data_type
        if 'basic_data_type' in table_extra_validations.keys():
            data_type = table_extra_validations["basic_data_type"]

        # Validate extra conditions of the custom_data_type
        if 'extra' in table_extra_validations.keys():
            if (table_extra_validations["extra"] != None):
                # In case the basic_data_type is decimal, we need to check the decimal point and the number of decimals
                if data_type == "decimal":
                    if 'decimal_point' in table_extra_validations["extra"].keys():
                        if table_extra_validations["extra"]["decimal_point"] == '.':
                            val = validate_extra("^.*\\" + str(table_extra_validations["extra"]["decimal_point"]) + ".*$", str(value), "decimal point not found ", table_extra_validations["extra"]["decimal_point"])
                            if (val != None):
                                return val
                        elif table_extra_validations["extra"]["decimal_point"] == ',':
                            val = validate_extra("^.*\\" + str(table_extra_validations["extra"]["decimal_point"]) + ".*$", str(value), "decimal point not found ", table_extra_validations["extra"]["decimal_point"])
                            if (val != None):
                                return val
                            value = str(value).replace(",",".")
                        
                    if 'n_decimals' in table_extra_validations["extra"].keys():
                        if table_extra_validations["extra"]["n_decimals"] == '.':
                            val =validate_extra("^\d*\.\d{" + str(table_extra_validations["extra"]["n_decimals"]) + "}$", str(value), "value doesn't have correct number of decimals ", table_extra_validations["extra"]["n_decimals"])
                            if (val != None):
                                return val
                        elif table_extra_validations["extra"]["n_decimals"] == ',':
                            val =validate_extra("^\d*\,\d{" + str(table_extra_validations["extra"]["n_decimals"]) + "}$", str(value), "value doesn't have correct number of decimals ", table_extra_validations["extra"]["n_decimals"])
                            if (val != None):
                                return val
                
                if 'max_length' in table_extra_validations["extra"].keys():
                    val = validate_extra("^.{1," + table_extra_validations["extra"]["max_length"] + "}$",str(value), "value is longer than ", table_extra_validations["extra"]["max_length"] )
                    if (val != None):
                        return val
                    
                if 'starting_with' in table_extra_validations["extra"].keys():
                    val = validate_extra("^"+table_extra_validations["extra"]["starting_with"],value, "value doesn't start with ", table_extra_validations["extra"]["starting_with"])
                    if (val != None):
                        return val
                    
                if 'ending_with' in table_extra_validations["extra"].keys():
                    val = validate_extra(""+table_extra_validations["extra"]["ending_with"] + "$", value, "value doesn't end with ", table_extra_validations["extra"]["ending_with"])
                    if (val != None):
                        return val
                
                if 'contains' in table_extra_validations["extra"].keys():
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
                return e
        case "integer":
            reg = '^[-+]?\d+$'
            try:
                val = RegexValidator(reg, "please provide an integer number", "Wrong integer format")
                re = val(value)
                return True
            except ValidationError as e:
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
                return exception

def validate_extra(regex_value, value, message, test_value):
    try:
        val = RegexValidator(regex_value, message + test_value , "")
        re = val(value)
        return re
    except ValidationError as e:
        return e
    
def valid_url(value:str) -> bool:
    try:
        URLValidator(value)
        return True
    except ValidationError as exception:
        return False
    
def valid_decimal(value:str, decimal_places = None) -> bool:
    try:
        if (decimal_places != None):
            DecimalValidator(value, decimal_places=decimal_places)
        else:
            DecimalValidator(value)
        return True
    except ValidationError as exception:
        return False
    
def regex_validator(reg,  message, code):
    return RegexValidator(regex = reg, message= message, code=code)