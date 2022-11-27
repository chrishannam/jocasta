import json

from influxdb_client import InfluxDBClient
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS
import logging
import platform
from typing import Dict, List

logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

logger = logging.getLogger(__name__)


class InfluxDBConnector:
    def __init__(self, url: str, token: str, org: str, bucket: str):

        self.client = InfluxDBClient(url=url, token=token, org=org)
        self.org = org
        self.bucket = bucket
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)

    def send(self, data: Dict, hostname: str = None) -> None:
        """
        Send the data over to the Influx server.
        """
        logger.info('Sending payload to InfluxDB server')
        self.send_payload(data, hostname=hostname)
        logger.info('Payload sent')

    def send_tapo(self, section, data, device_name=None):

        for name, value in data.items():
            point = (
                Point(device_name)
                .tag("host", device_name)
                .tag('reading', section)
                .field("value", float(value))
            )
            self.write_api.write(bucket=self.bucket, org=self.org, record=point)

    def send_payload(self, data: Dict, hostname: str = None) -> bool:
        """
        Break out each reading into measurements that Influx will understand.
        """
        logger.info('Building payload for Influxdb')

        # location isn't a measurement we want to log.
        location = data.pop('location', 'unset location')

        if not hostname:
            hostname = platform.node()

        for name, value in data.items():
            # payload = {
            #     'measurement': name,
            #     'tags': {'host': hostname, 'location': location},
            #     'fields': {'value': float(value)},
            # }
            point = (
                Point('office')
                .tag("reading", name)
                .tag("host", hostname)
                .tag('location', location)
                .field("value", value)
            )
            self.write_api.write(bucket=self.bucket, org=self.org, record=point)

        return True
