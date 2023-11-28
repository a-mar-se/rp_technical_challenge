Technical Challenge

Run react server
cd ./csv_upload_front
npm start

Run Django server (backend)
cd ./csv_upload_back
python3 manage.py runserver

Open Swagger documentation
One the Django server is running on port 8000, go to http://localhost:8000/csv_validation/swagger/ to see the documentation.

Run validation tests
cd ./csv_upload_back
python3 manage.py test