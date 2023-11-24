from django.core.exceptions import ValidationError
from django.core.validators import URLValidator, DecimalValidator, RegexValidator

def data_type_validator(value, data_type, n_decimals = None):
    match data_type:
        case "decimal":
            # decimal_regex()
            print('decimal')
            # valid_decimal(value)
            reg = "\d\.\d"
            try:
                val = RegexValidator(reg, "please provide a decimal number", "Wrong decimal format")
                re = val(value)
                print(re)
                return True
            except ValidationError as e:
                print(e)
                return e
                
            # print(value)
            # print(re)
            # return val(value)
        case "integer":
            print('integer')
            reg = "\d"
            try:
                val = RegexValidator(reg, "please provide a decimal number", "Wrong decimal format")
                re = val(value)
                print(re)
                return True
            except ValidationError as e:
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
                URLValidator(value,"Please provide a valid url")
                # url is valid here
                # do something, such as:
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
                URLValidator(value,"Please provide a valid url")
                # url is valid here
                # do something, such as:
                return True
            except ValidationError as exception:
                # URL is NOT valid here.
                # handle exception..
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