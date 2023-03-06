from time import sleep
from typing import Dict

import click
import logging

from prettytable import PrettyTable

from jocasta.config import load_config
from jocasta.inputs.serial_connector import ArduinoConfiguration
from jocasta.inputs.serial_connector import ArduinoReading
from jocasta.inputs.serial_connector import ArduinoSensorConnector

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)


@click.command()
@click.option('--forever', '-f', default=False, is_flag=True)
@click.option('--config-file', '-c', required=False, type=click.Path(exists=True))
@click.option('--device', '-d', required=False, type=click.Path(exists=True))
def main(forever, config_file, device):
    logger = logging.getLogger(__name__)

    logger.info('Starting')
    if config_file:
        logger.info('Using %s configuration file', config_file)
        configuration = load_config(config_file)
        arduino_configuration = ArduinoConfiguration(device=configuration.inputs.arduino.serial_port)
    else:
        arduino_configuration = ArduinoConfiguration(device=device)

    connector = ArduinoSensorConnector(arduino_configuration)
    logger.info('Sensor connected')

    if forever:
        while True:
            reading = get_reading(connector)
            display_output(reading=reading)
            sleep(2)
    else:
        reading = get_reading(connector)
        display_output(reading=reading)


def get_reading(connector: ArduinoSensorConnector):
    return connector.get_reading()


def display_output(reading: ArduinoReading):
    table = PrettyTable()
    table.field_names = reading.schema().get('properties').keys()
    table.add_row(list(reading.dict().values()))
    print(table)


if __name__ == '__main__':
    main()
