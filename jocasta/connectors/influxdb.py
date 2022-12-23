import json

from influxdb_client import InfluxDBClient
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS
import logging
import platform
from typing import Dict, List

from jocasta.config import InfluxDBConfiguration

logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

logger = logging.getLogger(__name__)


class InfluxDBConnector:
    def __init__(self, configuration: InfluxDBConfiguration):

        self.client = InfluxDBClient(url=configuration.url,
                                     token=configuration.token,
                                     org=configuration.org
                                     )
        self.org = configuration.org
        self.bucket = configuration.bucket
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)

    def send(self, data: Dict, hostname: str, location: str) -> None:
        """
        Send the data over to the Influx server.
        """
        logger.info('Sending payload to InfluxDB server')
        self.send_payload(data, hostname=hostname, location=location)
        logger.info('Payload sent')

    def send_tapo(self, data, name):

        for field, value in data.items():
            logger.info('Sending: %s -> %s', field, value)
            for k, v in value.items():
                point = (
                    Point(name)
                    .tag('reading_type', field)
                    .tag('time_range', k)
                    .field("value", float(v))
                )
                self.write_api.write(bucket=self.bucket, org=self.org, record=point)

    def send_payload(self, data: Dict, hostname: str, location: str = None) -> bool:
        """
        Break out each reading into measurements that Influx will understand.
        """
        logger.info('Building payload for Influxdb')

        for name, value in data.items():
            point = (
                Point('office')
                .tag("reading", name)
                .tag("hostname", hostname)
                .tag("location", location)
                .field("value", value)
            )
            self.write_api.write(bucket=self.bucket, org=self.org, record=point)

        return True
