from django.forms import FloatField
from rest_framework.serializers import ModelSerializer,  CharField
from .models import  Entity
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator, DecimalValidator, RegexValidator
from django.forms import DecimalField, IntegerField
import math
import json
from rest_framework import serializers


class EntitySerializer (ModelSerializer):     
    entity_id = CharField(max_length=8)
    data_type = CharField(max_length=16)
    data_value = CharField(max_length=256)
    table_extra_validations = CharField(max_length=256)

    class Meta: 
    
        model = Entity
        fields = '__all__'


    # def entity_validator(value, data_type, table_extra_validations = None):
    def validate_data_value(self, value):
        data = self.get_initial() # data for all the fields
        
        # return value
        if type(value) == "number":
        
            if math.isnan(value):
                return "value is empty"
        if len(str(value)) == 0:
            return "value is empty"
        
        table_extra_validations = json.loads(data["table_extra_validations"])
        data_type = data["data_type"]

        # if (table_extra_validations["basic_data_type"] != None):
        if hasattr(table_extra_validations, 'basic_data_type'):
            data_type = table_extra_validations["basic_data_type"]

        if hasattr(table_extra_validations, 'extra'):
        # if (table_extra_validations["extra"] != None):
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
                    raise ValidationError(message="Please provide a decimal number", code="Wrong decimal format")
            case "integer":
                reg = '^[-+]?\d+$'
                try:
                    val = RegexValidator(reg, "please provide an integer number", "Wrong integer format")
                    re = val(value)
                    return True
                except ValidationError as e:
                    raise ValidationError(message="Please provide a valid url", code="Wrong integer format")
            case "string":
                # decimal_regex()
                reg = "\w"
                try:
                    val = RegexValidator(reg, "please provide a string", "Wrong string format")
                    re = val(value)
                    return True
                except ValidationError as e:
                    raise ValidationError(message="Please provide a string", code="Wrong string format")
            case "url":
                try:
                    # alive_validator = URLValidator(verify_exists=True
                    vaa = URLValidator(message = "Please provide a valid url")
                    rf = vaa(value)
                    return True
                except ValidationError as exception:
                    raise ValidationError(message="Please provide a valid url", code="Wrong url format")


    # def validate_phone_number(self, value):
    #     rule = re.compile(r'(^[+0-9]{1,3})*([0-9]{10,11}$)')
    #     if not rule.search(value):
    #         raise serializers.ValidationError("Invalid Phone Number")
    #     return value


def validate_extra(regex_value, value, message, test_value):
    try:
        val = RegexValidator(regex_value, message + test_value , "")
        re = val(value)
        return re
    except ValidationError as e:
        return e
    