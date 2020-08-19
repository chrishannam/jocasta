from Adafruit_IO import Client
import logging

from jocasta.connectors.constants import HUMIDITY, LIGHT, TEMPERATURE

logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

logger = logging.getLogger(__name__)


class IOAdafruitConnector(object):
    def __init__(self, key, username, feeds) -> None:
        self.aio = Client(username=username, key=key)
        self.feeds = feeds

    def send(self, data):
        for feed in self.feeds.split(','):
            logger.info(f'Sending {feed} to AdaFruit.')
            if HUMIDITY in feed:
                self.aio.send_data(feed, data[HUMIDITY])
            if LIGHT in feed:
                self.aio.send_data(feed, data[LIGHT])
            if TEMPERATURE in feed:
                self.aio.send_data(feed, data[TEMPERATURE])
