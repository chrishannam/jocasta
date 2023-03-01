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
            output.send(readings=readings, hostname=platform.node(), location=self.config.location)

    #
    # def get_reading(connectors, sensor_reader, configs):
    #
    #     reading = sensor_reader.read()
    #     display_table(reading)
    #
    #     location = configs.local.location
    #     hostname = platform.node()
    #
    #     if reading:
    #         for conn in connectors.connectors:
    #             logger.debug(f'Reading: {reading}')
    #
    #             if hasattr(connectors, 'temperature_ranges'):
    #                 reading = validate_temperature(reading=reading, valid_range=connectors.temperature_ranges)
    #             conn.send(data=reading, location=location, hostname=hostname)
    #     else:
    #         print('Unable to get reading.')
    #
    #
    # def display_table(reading: Dict):
    #     table_data = [
    #         [i.capitalize() for i in reading.keys()],
    #         [i for i in reading.values()],
    #     ]
    #     print(tabulate(table_data, tablefmt='fancy_grid'))



