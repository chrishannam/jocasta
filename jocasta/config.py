"""
Configurations models for service setup.

Currently supports:
    * Kafka
    * InfluxDB

By default, the config should be located in ~/.config/race_strategist/config.ini

Example file:
[influxdb]
host = 192.168.0.101:8086
token = 8DxTEtW0PoCypTmxzXbSzTn8xPF39iiIVvW9bkvmf2wK2i6yth26dy-TabZp5IBAk
org = F1
bucket = telemetry_2020

[kafka]
bootstrap_servers = 192.168.0.102:9092
"""

import configparser

from pathlib import Path
from dataclasses import dataclass
import logging
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

from jocasta.connectors.file_system import FileSystemConfiguration
from jocasta.connectors.file_system import FileSystemConnector
from jocasta.connectors.influxdb import InfluxDBConfiguration
from jocasta.connectors.influxdb import InfluxDBConnector
from jocasta.connectors.kafka import KafkaConfiguration
from jocasta.connectors.kafka import KafkaConnector
from jocasta.connectors.tapo import TapoConfiguration
from jocasta.connectors.tapo import TapoConnector
from jocasta.connectors.tapo import TapoPlug
from jocasta.inputs.pimoroni_garden_board.co2 import CO2Sensor
from jocasta.inputs.serial_connector import ArduinoConfiguration
from jocasta.inputs.serial_connector import ArduinoSensorConnector

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

logger = logging.getLogger(__name__)

HOME: Path = Path.home()
CONFIG_FILE_NAME: str = 'jocasta.ini'


@dataclass
class LocalConfiguration:
    location: Optional[str] = None
    temperature_max: Optional[float] = None
    temperature_min: Optional[float] = None


@dataclass
class OutputConnectors:
    kafka: Union[KafkaConnector, None] = None
    influxdb: Union[InfluxDBConnector, None] = None
    file_system: Union[FileSystemConfiguration, None] = None

    def enabled_connectors(self) -> List:
        connectors_enabled = []
        for i in ['kafka', 'influxdb', 'file_system']:
            conn = getattr(self, i)
            if conn:
                connectors_enabled.append(conn)
        return connectors_enabled


@dataclass
class InputConnectors:
    arduino: Union[ArduinoSensorConnector, None] = None
    garden_co2: Union[CO2Sensor, None] = None
    tapo_plugs: Union[TapoConnector, None] = None

    def get_arduino_reading(self):
        if self.arduino:
            return self.arduino.get_reading()
        return None

    def get_garden_co2_reading(self):
        if self.garden_co2:
            return self.garden_co2.get_reading()
        return None

    def get_tapo_plug_reading(self):
        if self.tapo_plugs:
            return self.tapo_plugs.get_reading()
        return None


@dataclass
class Configuration:
    inputs: InputConnectors
    outputs: OutputConnectors
    configuration: LocalConfiguration


def load_config(filename=None) -> Configuration:
    if not filename:
        filename: Path = HOME / '.config' / CONFIG_FILE_NAME

    config = configparser.ConfigParser()
    config_file = Path(filename)
    configuration = Configuration(
        inputs=InputConnectors(),
        outputs=OutputConnectors(),
        configuration=LocalConfiguration(),
    )

    if config_file.is_file():
        config.read(filename)
    else:
        logger.warning('Unable to find config file.')
        return configuration

    for section in config.keys():
        # outputs
        if section == 'kafka':
            configuration.outputs.kafka = KafkaConnector(KafkaConfiguration(
                    bootstrap_servers=config[section]['bootstrap_servers'],
                    topics=config[section]['topics']
                )
            )

        elif section == 'influxdb':
            configuration.outputs.influxdb = InfluxDBConnector(InfluxDBConfiguration(
                    url=config[section]['url'],
                    token=config[section]['token'],
                    org=config[section]['org'],
                    bucket=config[section]['bucket'],
                )
            )

        elif section == 'file_system':
            configuration.outputs.file_system = FileSystemConnector(
                FileSystemConfiguration(config[section]['filename'])
            )

        # Inputs
        elif section == 'arduino':
            configuration.inputs.arduino = ArduinoSensorConnector(ArduinoConfiguration(device=config[section]['device']))

        elif section == 'pimoroni_garden':
            configuration.inputs.garden_co2 = CO2Sensor()

        elif section == 'tapo':
            plugs = []
            for plug in config[section].get('plugs', '').split(','):
                plugs.append(
                    TapoPlug(
                        name=plug.split(':')[0],
                        ipaddress=plug.split(':')[1],
                    )
                )

            configuration.inputs.tapo_plugs = TapoConnector(TapoConfiguration(
                email=config[section]['email'],
                password=config[section]['password'],
                plugs=plugs,
            ))

        elif section == 'local':
            configuration.configuration = LocalConfiguration(
                location=config[section]['location'],
                temperature_max=float(config[section].get('temperature_max', "50")),
                temperature_min=float(config[section].get('temperature_min', "-10")),
            )

    return configuration