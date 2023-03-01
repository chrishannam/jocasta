import json
import logging
from dataclasses import dataclass
from typing import List

from tapo_plug import tapoPlugApi


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s.%(msecs)03d %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


@dataclass
class TapoPlug:
    name: str
    ipaddress: str


@dataclass
class TapoConfiguration:
    plugs: List[TapoPlug]
    email: str
    password: str


class TapoConnector:
    """
    Send the packets as JSON to Kafka.
    """

    def __init__(self, configuration: TapoConfiguration):
        self.email = configuration.email
        self.password = configuration.password
        self.plugs = configuration.plugs

    def get_reading(self):
        data = {}
        for plug in self.plugs:
            ip = plug.ipaddress
            device = {
                'tapoEmail': self.email,
                'tapoPassword': self.password,
                'tapoIp': ip
            }
            try:
                result = json.loads(tapoPlugApi.getPlugUsage(device))

                data[plug.name] = {}

                for name, reading in result['result'].items():
                    data[plug.name][name] = {}
                    for k, v in reading.items():
                        data[plug.name][name][k] = v

            except Exception as exc:
                logger.exception(exc)
        return data

    def send(self, *_, **__):
        """ Not used"""
        pass
