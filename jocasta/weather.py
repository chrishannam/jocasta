from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
import json
from config import URL, TOKEN, ORG, BUCKET
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import json
import logging
from json import JSONDecodeError
import asyncio
from tapo import ApiClient


if __name__ == "__main__":
    owm = OWM('b0f7c64a5f517f0d157b6a5a9c720157')
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place('Beverley,GB')
    w = observation.weather

    client = influxdb_client.InfluxDBClient.from_config_file("/home/channam/code/jfdi/config.ini")
    write_api = client.write_api(write_options=SYNCHRONOUS)

    points = []
    print(w.rain)
    points.extend([
        Point("Weather")
            .tag("type", "open weather map")
            .field('pressure', w.pressure['press']),
        Point("Weather")
            .tag("type", "open weather map")
            .field('wind_speed', w.wnd['speed']),
        Point("Weather")
            .tag("type", "open weather map")
            .field('wind_direction', w.wnd['deg']),
        Point("Weather")
            .tag("type", "open weather map")
            .field('detailed_status', w.detailed_status),
        Point("Weather")
            .tag("type", "open weather map")
            .field('status', w.status),
        Point("Weather")
            .tag("type", "open weather map")
            .field('rain_amount', w.rain.get('1h', 0.0)),
        Point("Weather")
            .tag("type", "open weather map")
            .field('humidity', w.humidity)
       ])

    for name, value in w.temperature('celsius').items():
        if not value:
            continue

        points.extend([
            Point("Weather")
            .tag("type", "open weather map")
            .field(name, value)
            ])
        print(f"{name} -> {value} sent")
    write_api.write(bucket=BUCKET, org=ORG, record=points)

    print("Complete!")

    with open('/tmp/weather.json', 'w') as filename:
        json.dump(w.temperature('celsius'), filename, indent=4)

