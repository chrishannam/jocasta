"""
Generic collector code to run config file
"""
import platform
from dataclasses import dataclass
from time import sleep
from typing import Dict
from typing import Optional

from tabulate import tabulate

from jocasta.config import InputConnectors
from jocasta.config import OutputConnectors
from jocasta.config import load_config

import click
import logging

from jocasta.validators import validate_temperature

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


@click.command()
@click.option('--port', '-p', type=click.Path(exists=True))
@click.option('--forever', '-f', default=False, is_flag=True)
@click.option('--config-file', '-c', required=False, type=click.Path(exists=True))
@click.option('--log-level', '-l', default='error')
def main(port, forever, config_file, log_level):

    level = LEVELS.get(log_level)
    logging.basicConfig(
        level=level,
        format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    for logg in loggers:
        logg.setLevel(level)

    logger.debug('Starting...')
    output_connectors, input_connections = load_config(config_file)

    if forever:
        while True:
            try:
                arduino_reading = input_connections.arduino.get_reading()
                tapo_reading = input_connections.get_tapo_plugs_readings()
                sleep(1)
            except Exception as esc:
                logger.exception(esc)
    else:
        readings = get_readings(input_connections)
        if readings.arduino:
            print(readings.arduino)
        if readings.tapo:
            print(readings.tapo)
        if readings.garden:
            print(readings.garden)


@dataclass
class Readings:
    arduino: Optional[Dict] = None
    tapo: Optional[Dict] = None
    garden: Optional[Dict] = None


def get_readings(input_connections: InputConnectors):

    return Readings(
        arduino=input_connections.get_arduino_reading(),
        tapo=input_connections.get_tapo_plug_reading(),
        garden=input_connections.get_garden_co2_reading(),
    )


def get_reading(connectors, sensor_reader, configs):

    reading = sensor_reader.read()
    display_table(reading)

    location = configs.local.location
    hostname = platform.node()

    if reading:
        for conn in connectors.connectors:
            logger.debug(f'Reading: {reading}')

            if hasattr(connectors, 'temperature_ranges'):
                reading = validate_temperature(reading=reading, valid_range=connectors.temperature_ranges)
            conn.send(data=reading, location=location, hostname=hostname)
    else:
        print('Unable to get reading.')


def display_table(reading: Dict):
    table_data = [
        [i.capitalize() for i in reading.keys()],
        [i for i in reading.values()],
    ]
    print(tabulate(table_data, tablefmt='fancy_grid'))


if __name__ == '__main__':
    main()
