import json
import logging
from typing import Dict

from jocasta.config import KafkaConfiguration
from confluent_kafka import Producer


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s.%(msecs)03d %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


class KafkaConnector:
    """
    Send the packets as JSON to Kafka.
    """

    def __init__(self, configuration: KafkaConfiguration):
        self.producer = Producer({'bootstrap.servers': configuration.bootstrap_servers})
        self.topics = {}
        for i in configuration.topics.split(','):
            self.topics[i.split(':')[0]] = i.split(':')[1]

    def send(self, data):
        for reading, value in data.items():
            d = {reading: value}
            self.producer.produce(self.topics[reading], json.dumps(d).encode())
        self.producer.flush()
