from fastapi import FastAPI
import json

app = FastAPI()


@app.get("/")
async def root():

    with open('/tmp/sensor_data.json') as json_file:
        data = json.load(json_file)
    return data
