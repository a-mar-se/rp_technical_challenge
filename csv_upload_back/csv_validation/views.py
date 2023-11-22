from rest_framework.views import APIView;
from rest_framework.response import Response;
import csv;
import pathlib;
import pandas;
import json;
from .serializer import EntitySerializer;

class ValidateView(APIView):
    def post(self, request):
        # print(request.data)
        # print(request.data["file"])

        csv_file = request.data["file"]
        csv_file = request.FILES["file"]
        data_types_table = json.loads(request.data["table"])
        response = Response()

        # print(csv_file)
        r = pandas.read_csv(csv_file)
        csv_records = len(r.index)
        print(csv_records)
        # print(r.iloc[0])

        for element_index in range(csv_records):
            element = r.iloc[element_index]
            print(element)
            for dt_index in range(len(data_types_table)):
                dt_checked = data_types_table[dt_index]
                print(dt_checked)
                print(dt_checked["data_type"])
                print(element["data_type"])
                if element["data_type"] == dt_checked["data_type"]:
                    print("true")
                else:
                    print("fgalse")
        
        # re = csv_file.read()
        # print(re)
        # with open(csv_file.temporary_file_path(), 'r') as file_obj: 
        #     print(', '.join(file_obj))
        # spamreader = csv.reader(csv_file, delimiter=',')
        # print(spamreader)
        # ifile  = open(csv_file, "rt", encoding=<theencodingofthefile>)
        # for row in spamreader:
        #     print(', '.join(row))
        response.data = {
            'message' : "validating csv file..."
        }
        return response

