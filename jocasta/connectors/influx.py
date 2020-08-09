from influxdb import InfluxDBClient
from datetime import datetime
import logging
import platform
from typing import Dict, List

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

logger = logging.getLogger(__name__)


class InfluxDBConnector(object):
    def __init__(self, database, password, username, host=None, port=None):

        if not host:
            host = 'localhost'

        if not port:
            port = 8086

        self.influx_client = InfluxDBClient(host, port, username, password, database)

    def send(self, data: Dict) -> None:
        """
        Send the data over to the Influx server.
        """
        json_payload = _build_payload(data)
        self.influx_client.write_points(json_payload)


def _build_payload(data: Dict) -> List:
    """
    Break out each reading into measurements that Influx will understand.
    """
    logger.info('Build payload for Influxdb')
    payload_values = []

    # location isn't a measurement we want to log.
    location = data.pop('location', 'unknown location')

    time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

    for name, value in data.items():
        payload = {
            'measurement': name,
            'tags': {'host': platform.node(), 'location': location},
            'time': time,
            'fields': {'value': value},
        }
        payload_values.append(payload)
    return payload_values
