<h1>RavenPack Technical Challenge: Cloud FullStack Developer</h1>

<h4>Run react server</h4>
<p>cd ./csv_upload_front</p>
<p>npm start</p>

<h4>Run Django server (backend)</h4>
<p>cd ./csv_upload_back</p>
<p>python3 manage.py runserver</p>

<h4>Run Django server with Docker</h4>
<p>cd ./csv_upload_back</p>
<p>docker build -t django-csv .</p>
<p>docker run -it -p 8000:8000 django-csv</p>

<h4>Open Swagger documentation</h4>
<p>One the Django server is running on port 8000, go to http://localhost:8000/csv_validation/swagger/ to see the documentation.</p>

<h4>Run validation tests</h4>
<p>cd ./csv_upload_back</p>
<p>python3 manage.py test</p>


<h2>How to use this tool?</h2>
<p>Once the servers are running go to http://localhost:3000/ (3000 being the react port). </p>
<p>There are 4 simple data_types: decimal, integer, string and url.</p>
<p>To create new data_types, click on "Add new custom data_type". A pop up will open that allows us to create a new data_type on the UI. We can configure the data_type name, decription (only informative), basic_data_type and extra validation conditions. To add extra conditions, select one on the dropdown and type the value on the text input, then click "Add extra validation".</p>
<p>If you have already defined all extra conditions on your custom data_type, click "Create data_type: "{data_type_name}" to store the info. The pop up closes and you can see your defined custom_data_type on the Data_type table. </p>

<p>Then you can browse your csv file, and validate the values clicking "Validate using serializer" of "Validate using validator". If there are any errors, information about them can be seen on table on the UI. If everything looks fine on your csv file, you will see "All in order on your csv file" on the screen.</p>


Many thanks for this opportunity, it was a challenging test!