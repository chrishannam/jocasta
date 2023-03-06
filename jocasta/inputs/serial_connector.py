"""
Read data from serial port.
By default we assume the data coming over the serial port
is JSON.

This can be changed to expect csv by:

sensor = SerialSensor(port='ttyUSB0', json_data=False)
"""

import glob
import json
import logging
from dataclasses import dataclass
from json import JSONDecodeError
from typing import Optional

import serial
import os.path
import time
from pydantic import BaseModel


# usual linux ports
PORTS = ['ttyUSB0', 'ttyUSB1', 'ttyAMA0', 'ttyACM0']
SERIAL_PORT_PATH_ROOT = '/dev/'


logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

logger = logging.getLogger(__name__)


class ArduinoReading(BaseModel):
    temperature: float
    humidity: float
    light: float


@dataclass
class ArduinoConfiguration:
    device: str


class ArduinoSensorConnector:
    def __init__(self, config: ArduinoConfiguration = None, json_data=True, debug=True):
        if config.device:
            self.serial_port = config.device
        else:
            logger.info('Finding port.')
            self.serial_port = _detect_port()
        self.ser = serial.Serial(self.serial_port, 9600, timeout=1)

        self.debug = debug
        self.json_data = json_data

        logger.debug(f'Using {self.serial_port} as serial port')

    def get_reading(self, timeout=10):

        if not self.serial_port:
            logger.error('Unable to find anything on the serial port to read from.')
            return

        stop = time.time() + timeout
        i = 0

        while time.time() < stop:
            i = i + 1
            raw_serial = self.ser.readline()

            logger.debug(f'Attempt {i}: Received: {raw_serial}')

            if self.json_data and raw_serial:
                if reading := self.convert_to_reading(raw_serial):
                    return reading
            else:
                logger.debug('Failed to decode anything')

    def convert_to_reading(self, raw_serial) -> Optional[ArduinoReading]:
        try:
            return ArduinoReading(**json.loads(raw_serial))
        except JSONDecodeError:
            logger.debug(f'Failed to decode to JSON: {raw_serial}')
        return None


def _detect_port():

    device_path = None

    for port in PORTS:
        device = SERIAL_PORT_PATH_ROOT + port
        if os.path.exists(device):
            device_path = device

    if not device_path:
        # let's try osx stuff
        for file_name in glob.glob1('/dev', 'tty.usbserial-*'):
            device_path = SERIAL_PORT_PATH_ROOT + file_name
    return device_path
