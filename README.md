<h1>RavenPack Technical Challenge: Cloud FullStack Developer</h1>

<h4>Run react server</h4>
cd ./csv_upload_front
npm start

<h4>Run Django server (backend)</h4>
cd ./csv_upload_back
python3 manage.py runserver

<h4>Run Django server with Docker</h4>
cd ./csv_upload_back
docker build -t django-csv .
docker run -it -p 8000:8000 django-csv

<h4>Open Swagger documentation</h4>
One the Django server is running on port 8000, go to http://localhost:8000/csv_validation/swagger/ to see the documentation.

<h4>Run validation tests</h4>
cd ./csv_upload_back
python3 manage.py test


<h2>How to use this tool?</h2>
Once the servers are running go to http://localhost:3000/ (3000 being the react port). 
There are 4 simple data_types: decimal, integer, string and url.
To create new data_types, click on "Add new custom data_type". A pop up will open that allows us to create a new data_type on the UI. We can configure the data_type name, decription (only informative), basic_data_type and extra validation conditions. To add extra conditions, select one on the dropdown and type the value on the text input, then click "Add extra validation".
If you have already defined all extra conditions on your custom data_type, click "Create data_type: "{data_type_name}" to store the info. The pop up closes and you can see your defined custom_data_type on the Data_type table. 

Then you can browse your csv file, and validate the values clicking "Validate using serializer" of "Validate using validator". If there are any errors, information about them can be seen on table on the UI. If everything looks fine on your csv file, you will see "All in order on your csv file" on the screen.


Many thanks for this opportunity, it was a challenging test!