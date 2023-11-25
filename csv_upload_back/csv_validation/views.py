from rest_framework.views import APIView;
from rest_framework.response import Response;
import csv;
import pathlib;
import pandas;
import json

from .validators import data_type_validator;
from .serializer import EntitySerializer;

class ValidateView(APIView):
    def post(self, request):
        
        csv_file = request.data["file"]
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
            response.data={'error':error_data}
        return response

