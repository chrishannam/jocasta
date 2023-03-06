"""
Generic collector code to run config file
"""
from dataclasses import dataclass
from typing import Dict
from typing import Optional


from jocasta.config import Configuration
import logging
import platform


LEVELS = {
    'critical': logging.CRITICAL,
    'error': logging.ERROR,
    'warn': logging.WARNING,
    'warning': logging.WARNING,
    'info': logging.INFO,
    'debug': logging.DEBUG,
}

logger = logging.getLogger(__name__)
loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]


@dataclass
class Readings:
    arduino: Optional[Dict] = None
    tapo: Optional[Dict] = None
    garden: Optional[Dict] = None

    def to_dict(self) -> Dict:
        return {
            'arduino': self.arduino,
            'tapo': self.tapo,
            'garden': self.garden,
        }


class Controller:

    def __init__(self, config: Configuration):
        self.inputs = config.inputs
        self.outputs = config.outputs
        self.config = config.configuration
        self.configuration = config

    def get_readings(self):
        """
        Collect all available readings
        """

        return Readings(
            arduino=self.inputs.get_arduino_reading(),
            tapo=self.inputs.get_tapo_plug_reading(),
            garden=self.inputs.get_garden_co2_reading(),
        )

    def send_readings(self, readings: Readings):
        for output in self.outputs.enabled_connectors():
            logger.info(f'Sending data to %s', output)
            output.send(readings=readings, hostname=platform.node(), location=self.config.location)
