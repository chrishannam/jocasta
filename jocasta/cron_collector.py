"""
Generic collector code to run config file
"""

from .inputs.serial_connector import SerialSensor
from .connectors import (dweet, file_system, io_adafruit, influx)
import configparser
from .command_line.setup import setup_config


def main():
    sensor_reader = SerialSensor()
    config = setup_config()

    reading = sensor_reader.read()
    connectors = {}

    for section in config.sections():
        if section == 'adafruit':
            connectors['adafruit'] = io_adafruit.IOAdafruitConnector(**)
        # if name == 'DWEET_NAME':
        #     conn = dweet.DweetConnector(setting)
        # elif name == 'ADAFRUITIO_KEY':
        #     conn = io_adafruit.IOAdafruitConnector(setting)
        # elif name == 'FILE_SYSTEM_PATH':
        #     conn = file_system.FileSystemConnector(setting)
        # elif name == 'INFLUXDB':
        #     conn = influx.InfluxDBConnector(setting)

        conn.send(reading)


if __name__ == "__main__":
    main()
