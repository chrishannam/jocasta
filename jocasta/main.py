"""
Generic collector code to run config file
"""

from jocasta.collector import Controller
from jocasta.collector import Readings
from jocasta.config import load_config

import click
import logging


loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
for logger in loggers:
    logger.setLevel(logging.INFO)


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

logger = logging.getLogger(__name__)


@click.command()
@click.option('--forever', '-f', default=False, is_flag=True)
@click.option('--config-file', '-c', required=False, type=click.Path(exists=True))
@click.option('--log-level', '-l', default='error')
def main(forever, config_file, log_level):

    logger.debug('Starting...')
    configuration = load_config(config_file)

    controller = Controller(config=configuration)

    if forever:
        while True:
            readings: Readings = controller.get_readings()
            print(f'Arduino: {readings.arduino}')
            print(f'Tapo: {readings.tapo}')
            print(f'Garden: {readings.garden}')
            controller.send_readings(readings=readings)

    else:
        readings: Readings = controller.get_readings()
        controller.send_readings(readings=readings)


if __name__ == '__main__':
    main()
