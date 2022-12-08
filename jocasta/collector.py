"""
Generic collector code to run config file
"""
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


@click.command()
@click.option('--port', '-p') # , type=click.Path(exists=True))
@click.option('--config-file', '-c', required=False, type=click.Path(exists=True))
@click.option('--log-level', '-l', default='error')
def main(port, config_file, log_level):

    configs = load_config(config_file)
    level = LEVELS.get(log_level)
    logging.basicConfig(
        level=level,
        format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    logger = logging.getLogger(__name__)
    loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
    for logger in loggers:
        logger.setLevel(level)

    logger.debug('Starting...')

    # sensor_reader = SerialSensor(port=port)
    # reading = sensor_reader.read()
    reading = {'light': 5.0, 'temperature': 16.0, 'humidity': 76.0}
    display_table(reading)

    if reading:
        connectors = EnabledConnectors(configs)
        for conn in connectors.connectors:
            logger.debug(f'Reading: {reading}')

            if hasattr(connectors, 'temperature_ranges'):
                reading = validate_temperature(reading=reading, valid_range=connectors.temperature_ranges)
            conn.send(data=reading)
    else:
        print('Unable to get reading.')


# def setup_cs(config):
#     connectors = {}
#     for name, section in config.items():
#         args = convert_config_stanza(section)
#         if name == 'csv_file':
#             connectors[name] = csv_file.CSVFileConnector(**args)
#         elif name == 'file_system':
#             connectors[name] = file_system.FileSystemConnector(**args)
#         elif name == 'io_adafruit':
#             connectors[name] = io_adafruit.IOAdafruitConnector(**args)
#         elif name == 'influxdb':
#             connectors[name] = influx.InfluxDBConnector(**args)
#         elif name == 'kafka':
#             connectors[name] = influx.InfluxDBConnector(**args)
#     return connectors


def display_table(reading: Dict):
    table_data = [
        [i.capitalize() for i in reading.keys()],
        [i for i in reading.values()],
    ]
    print(tabulate(table_data, tablefmt='fancy_grid'))


if __name__ == '__main__':
    main()
