import os

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from datetime import datetime
import json

app = FastAPI()

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other
    head content must come *after* these tags -->
    <title>Bootstrap 101 Template</title>

    <!-- Bootstrap -->
    <link href="css/bootstrap.min.css" rel="stylesheet">

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="https://cdn.jsdelivr.net/npm/html5shiv@3.7.3/dist/html5shiv.min.js"></script>
      <script src="https://cdn.jsdelivr.net/npm/respond.js@1.4.2/dest/respond.min.js"></script>
    <![endif]-->
  </head>
  <body>
    <h1>Last Run: {last_run}</h1>
    <h1>Temperature: {temperature}c</h1>
    <h1>Light: {light}</h1>
    <h1>Humidity: {humidity}</h1>
    <h1>Current Server Time: {now}</h1>

    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="js/bootstrap.min.js"></script>
  </body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
async def root():
    sensor_file = "/tmp/sensor_data.json"
    with open(sensor_file) as json_file:
        data = json.load(json_file)
        data["last_run"] = datetime.fromtimestamp(os.path.getmtime(sensor_file)).isoformat(" ", "seconds")
        data["now"] = str(datetime.now().isoformat(" ", "seconds"))
    return TEMPLATE.format(**data)
