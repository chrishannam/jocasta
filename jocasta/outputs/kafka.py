import json
import logging
from dataclasses import dataclass
from typing import Dict

from confluent_kafka import Producer


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s.%(msecs)03d %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


@dataclass
class KafkaConfiguration:
    bootstrap_servers: str
    topics: str


class KafkaConnector:
    """
    Send the packets as JSON to Kafka.
    """

    def __init__(self, configuration: KafkaConfiguration):
        self.producer = Producer({'bootstrap.servers': configuration.bootstrap_servers})

    def send(self, data: Dict, hostname: str, location: str):
        for reading, value in data.items():
            d = {
                reading: value,
                "location": location,
                "hostname": hostname,
            }
            topic = f'{location}.{reading}'
            self.producer.produce(topic, json.dumps(d).encode())
        self.producer.flush()
