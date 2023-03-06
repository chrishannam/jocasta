"""
Generic collector code to run config file
"""
import platform
from time import sleep

from jocasta.config import ConnectorsConfiguration
from jocasta.config import load_config
from jocasta.outputs.enabled_connectors import EnabledConnectors
from scd4x import SCD4X

import click
import logging

from jocasta.constants import InfluxdbPointNames

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
@click.option('--forever', '-f', default=False, is_flag=True)
@click.option('--config-file', '-c', required=False, type=click.Path(exists=True))
@click.option('--log-level', '-l', default='error')
def main(forever, config_file, log_level):

    level = LEVELS.get(log_level)
    logging.basicConfig(
        level=level,
        format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    for logg in loggers:
        logg.setLevel(level)

    logger.debug('Starting...')
    configs: ConnectorsConfiguration = load_config(config_file)
    connectors = EnabledConnectors(configs)
    sensor_reader = SCD4X(quiet=False)
    sensor_reader.start_periodic_measurement()

    if forever:
        while True:
            try:
                get_reading(connectors, sensor_reader, configs)
                sleep(5)
            except Exception as esc:
                logger.exception(esc)
    else:
        get_reading(connectors, sensor_reader, configs)


def get_reading(connectors, sensor_reader, configs):

    co2, temperature, relative_humidity, timestamp = sensor_reader.measure()

    location = configs.local.location
    hostname = platform.node()
    reading = {'CO2': co2}

    if co2:
        for conn in connectors.connectors:
            conn.send(name=InfluxdbPointNames.environment.value, data=reading, location=location, hostname=hostname)
    else:
        logger.error('Unable to get reading.')

    print(reading)


if __name__ == '__main__':
    main()
