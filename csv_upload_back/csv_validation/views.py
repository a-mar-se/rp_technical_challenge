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


class ValidateView(APIView):
    @swagger_auto_schema(
        operation_description="Validate values from s CSV file uploaded",
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

                        'description': openapi.Schema(type=openapi.TYPE_STRING, description="Description of the type"),
                        'extra': openapi.Schema(type = openapi.TYPE_OBJECT, properties={
                            'starts_with': openapi.Schema(type=openapi.TYPE_STRING, description="Optional validation condition: starting with characters ..."),
                            'ending_with': openapi.Schema(type=openapi.TYPE_STRING, description="Optional validation condition: ending with characters ..."),
                            'max_length': openapi.Schema(type=openapi.TYPE_STRING, description="Optional validation condition: maximum length in characters ..."),
                            'contains': openapi.Schema(type=openapi.TYPE_STRING, description="Optional validation condition: containes characters ..."),
                            'decimal_point': openapi.Schema(type=openapi.TYPE_STRING, description="Optional validation condition for decimal-based data_types: is the decimal point . or ,?"),
                            'n_decimals': openapi.Schema(type=openapi.TYPE_STRING, description="Optional validation condition for decimal-based data_types: how many decimals shoudld each value have?")
                        }),
                        'basic_data_type': openapi.Schema(type=openapi.TYPE_STRING, description="Basic data_type for custom data_types"),
                    }
                ),
            },
            required=['file'],
            
        )
    )


    # data_type: name, 
    # description: description, 
    # extra:Object.keys(extraValidations).length > 0 ? extraValidations : null,
    # basic_data_type: selectedOption?.value

    def post(self, request):
        
        csv_file = request.FILES["file"]
        data_types_table = json.loads(request.data["table"])
        response = Response()

        # print(csv_file)
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
                    # Check validations depending on the data type
                    validation = data_type_validator(element["data_value"],dt_checked["data_type"], data_types_table[dt_index])
                    if (validation != True):
                        str_val = str(validation)
                        print(str_val)
                        error_data.append({"value": str(element["data_value"]),"entity_id": element["entity_id"], "data_type": element["data_type"], "error_description": str_val})
                        # error_data.append("ValidationError: Entity_id \'" + element["entity_id"] + "\' with data_type '" + element["data_type"] + "'. " + str_val)
                    
                
            if data_type_found == False:
                error_data.append({"value": str(element["data_value"]),"entity_id": element["entity_id"], "data_type": element["data_type"], "error_description": "has a data_type not defined. Define the data_type on the table above to validate."})
                # response.data({'error': 'Record ' + element["entity_id"] + ' has a data_type not defined: ' + element["data_type"]})
        # response.data = {
        #     'message' : "validating csv file..."
        # }
        print(error_data)
        if len(error_data) != 0:
            response.status_code = 202
            response.data={'error':error_data}
        return response
