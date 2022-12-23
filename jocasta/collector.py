"""
Generic collector code to run config file
"""
import platform
from typing import Dict

from tabulate import tabulate

from jocasta.config import load_config
from jocasta.connectors.enabled_connectors import EnabledConnectors
from jocasta.inputs.serial_connector import SerialSensor

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
@click.option('--forever', '-f', default=False, required=False)
@click.option('--config-file', '-c', required=False, type=click.Path(exists=True))
@click.option('--log-level', '-l', default='error')
def main(port, forever, config_file, log_level):

    level = LEVELS.get(log_level)
    logging.basicConfig(
        level=level,
        format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    for logger in loggers:
        logger.setLevel(level)

    logger.debug('Starting...')
    configs = load_config(config_file)
    connectors = EnabledConnectors(configs)
    sensor_reader = SerialSensor(port=port)

    if forever:
        while True:
            try:
                get_reading(connectors, sensor_reader, configs)
            except Exception as esc:
                logger.exception(esc)
    else:
        get_reading(connectors, sensor_reader, configs)


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
