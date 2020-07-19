"""
Generic collector code to run config file
"""

from jocasta.inputs.serial_connector import SerialSensor

from jocasta.connectors import file_system

# io_adafruit, influx
from jocasta.command_line.setup import setup_config, convert_config_stanza
import click
import logging


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

logger = logging.getLogger(__name__)


@click.command()
@click.argument('port')
def main(port):
    sensor_reader = SerialSensor(port=port)
    config = setup_config()

    reading = sensor_reader.read()
    logging.info(reading)
    connectors = {}

    for name, section in config.items():
        print(name)
        args = convert_config_stanza(section)
        if name == 'file_system':
            connectors['file_system'] = file_system.FileSystemConnector(**args)
        # elif name == 'adafruit':
        #     connectors['adafruit'] = io_adafruit.IOAdafruitConnector(**args)
        # elif name == 'influxdb':
        #     connectors['influxdb'] = influx.InfluxDBConnector(**args)
    # elif name == 'file_system':
    #     connectors['file_system'] = file_system.FileSystemConnector(**args)
    # if name == 'DWEET_NAME':
    #     conn = dweet.DweetConnector(setting)
    # elif name == 'ADAFRUITIO_KEY':
    #     conn = io_adafruit.IOAdafruitConnector(setting)
    # elif name == 'FILE_SYSTEM_PATH':
    #     conn = file_system.FileSystemConnector(setting)
    # elif name == 'INFLUXDB':
    #     conn = influx.InfluxDBConnector(setting)
    connectors['file_system'].send(data=reading)


if __name__ == '__main__':
    logger.info('Starting...')
    main()
