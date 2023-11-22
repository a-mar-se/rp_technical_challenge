from rest_framework.views import APIView;
from rest_framework.response import Response;

class ValidateView(APIView):
    def post(self, request):
        print(request.data)
        print(request.data["file"])

        csv_file = request.data["file"]
        response = Response()
        response.data = {
            'message' : "validating csv file..."
        }
        return response

