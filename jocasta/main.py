"""
Generic collector code to run config file
"""

from jocasta.collector import Controller
from jocasta.collector import Readings
from jocasta.config import load_config

import click
import logging


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
    configuration = load_config(config_file)

    controller = Controller(config=configuration)

    if forever:
        while True:
            readings: Readings = controller.get_readings()
            controller.send_readings(readings=readings)
            a = 1
    # else:
    #     readings = get_readings(input_connections)
    #     if readings.arduino:
    #         print(readings.arduino)
    #     if readings.tapo:
    #         print(readings.tapo)
    #     if readings.garden:
    #         print(readings.garden)


if __name__ == '__main__':
    main()
