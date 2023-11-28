from rest_framework.views import APIView;
from rest_framework.response import Response;
import csv;
import pathlib;
import pandas;
import json

from .validators import data_type_validator;
from .serializer import EntitySerializer;

from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from django.core.exceptions import ValidationError


class ValidateSerializerView(APIView):
    @swagger_auto_schema(
        operation_description="Validate values from a CSV file uploaded",
        responses={
            200: "Validation checkes: Success. All values are validated successfully against their data_types.",
            202: "Validation checked: Not passed. One or more values are not validated successfully against their data_types.",
        },
        request_body=openapi.Schema(
            content="multipart/form-data",
            type=openapi.TYPE_OBJECT,
            properties={
                'file': openapi.Schema(
                    type=openapi.TYPE_STRING, description="CSV file"),
                'table': openapi.Schema(
                    type=openapi.TYPE_OBJECT, properties={
                        'data_type': openapi.Schema(type=openapi.TYPE_STRING, description="Data_type"),
                        'basic_data_type': openapi.Schema(type=openapi.TYPE_STRING, description="Basic data_type for custom data_types"),
                        'description': openapi.Schema(type=openapi.TYPE_STRING, description="Description of the type"),
                        'extra': openapi.Schema(type = openapi.TYPE_OBJECT, properties={
                            'starts_with': openapi.Schema(type=openapi.TYPE_STRING, description="Optional validation condition: starting with characters ..."),
                            'ending_with': openapi.Schema(type=openapi.TYPE_STRING, description="Optional validation condition: ending with characters ..."),
                            'max_length': openapi.Schema(type=openapi.TYPE_STRING, description="Optional validation condition: maximum length in characters ..."),
                            'contains': openapi.Schema(type=openapi.TYPE_STRING, description="Optional validation condition: containes characters ..."),
                            'decimal_point': openapi.Schema(type=openapi.TYPE_STRING, description="Optional validation condition for decimal-based data_types: is the decimal point . or ,?"),
                            'n_decimals': openapi.Schema(type=openapi.TYPE_STRING, description="Optional validation condition for decimal-based data_types: how many decimals shoudld each value have?")
                        }),
                    }
                ),
            },
            required=['file'],
            
        )
    )

    def post(self, request):
        
        csv_file = request.FILES["file"]
        data_types_table = request.data["table"]
        data_types_table = json.loads(request.data["table"])
        response = Response()

        r = pandas.read_csv(csv_file)
        csv_records = len(r.index)
        error_data = []

        for element_index in range(csv_records):
            element = r.iloc[element_index]
            data_type_found = False
            for dt_index in range(len(data_types_table)):
                dt_checked = data_types_table[dt_index]
                if element["data_type"] == dt_checked["data_type"]:
                    data_type_found = True

                    serializer = EntitySerializer(
                        data={
                            "entity_id":element["entity_id"],
                            "data_type":element["data_type"],
                            "data_value":str(element["data_value"]),
                            "table_extra_validations": json.dumps(data_types_table[dt_index])
                        }
                    )

                    try:
                        sd = serializer.is_valid(raise_exception=True)
                    except Exception as e:
                        for v in e.detail.values():
                            error_data.append({"value": str(element["data_value"]),"entity_id": element["entity_id"], "data_type": element["data_type"], "error_description": v[0]})
                        
                
            if data_type_found == False:
                error_data.append({"value": str(element["data_value"]),"entity_id": element["entity_id"], "data_type": element["data_type"], "error_description": "has a data_type not defined. Define the data_type on the table above to validate."})

        if len(error_data) != 0:
            response.status_code = 202
            response.data={'error':error_data}
        return response



class ValidatorView(APIView):
    @swagger_auto_schema(
        operation_description="Validate values from a CSV file uploaded",
        responses={
            200: "Validation checkes: Success. All values are validated successfully against their data_types.",
            202: "Validation checked: Not passed. One or more values are not validated successfully against their data_types.",
        },
        request_body=openapi.Schema(
            content="multipart/form-data",
            type=openapi.TYPE_OBJECT,
            properties={
                'file': openapi.Schema(
                    type=openapi.TYPE_STRING, description="CSV file"),
                'table': openapi.Schema(
                    type=openapi.TYPE_OBJECT, properties={
                        'data_type': openapi.Schema(type=openapi.TYPE_STRING, description="Data_type"),
                        'basic_data_type': openapi.Schema(type=openapi.TYPE_STRING, description="Basic data_type for custom data_types"),
                        'description': openapi.Schema(type=openapi.TYPE_STRING, description="Description of the type"),
                        'extra': openapi.Schema(type = openapi.TYPE_OBJECT, properties={
                            'starts_with': openapi.Schema(type=openapi.TYPE_STRING, description="Optional validation condition: starting with characters ..."),
                            'ending_with': openapi.Schema(type=openapi.TYPE_STRING, description="Optional validation condition: ending with characters ..."),
                            'max_length': openapi.Schema(type=openapi.TYPE_STRING, description="Optional validation condition: maximum length in characters ..."),
                            'contains': openapi.Schema(type=openapi.TYPE_STRING, description="Optional validation condition: containes characters ..."),
                            'decimal_point': openapi.Schema(type=openapi.TYPE_STRING, description="Optional validation condition for decimal-based data_types: is the decimal point . or ,?"),
                            'n_decimals': openapi.Schema(type=openapi.TYPE_STRING, description="Optional validation condition for decimal-based data_types: how many decimals shoudld each value have?")
                        }),
                    }
                ),
            },
            required=['file'],
            
        )
    )

    def post(self, request):
        
        csv_file = request.FILES["file"]
        data_types_table = request.data["table"]
        data_types_table = json.loads(request.data["table"])
        response = Response()
        r = pandas.read_csv(csv_file)
        csv_records = len(r.index)
        error_data = []

        for element_index in range(csv_records):
            element = r.iloc[element_index]
            data_type_found = False
            for dt_index in range(len(data_types_table)):
                dt_checked = data_types_table[dt_index]
                if element["data_type"] == dt_checked["data_type"]:
                    data_type_found = True

                    # Old validation
                    # Check validations depending on the data type
                    validation = data_type_validator(element["data_value"],dt_checked["data_type"], data_types_table[dt_index])
                    if (validation != True):
                        str_val = str(validation)
                        error_data.append({"value": str(element["data_value"]),"entity_id": element["entity_id"], "data_type": element["data_type"], "error_description": str_val})
                    
                
            if data_type_found == False:
                error_data.append({"value": str(element["data_value"]),"entity_id": element["entity_id"], "data_type": element["data_type"], "error_description": "has a data_type not defined. Define the data_type on the table above to validate."})

        if len(error_data) != 0:
            response.status_code = 202
            response.data={'error':error_data}
        return response

