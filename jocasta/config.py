"""
Configurations models for service setup.

Currently supports:
    * Kafka
    * InfluxDB

By default the config should be located in ~/.config/race_strategist/config.ini

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
from typing import Union

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

logger = logging.getLogger(__name__)

HOME: Path = Path.home()
CONFIG_FILE_NAME: str = 'jocasta.ini'


@dataclass
class KafkaConfiguration:
    bootstrap_servers: str
    topics: str


@dataclass
class InfluxDBConfiguration:
    url: str
    token: str
    org: str
    bucket: str


@dataclass
class FileSystemConfiguration:
    filename: str


@dataclass
class LocalConfiguration:
    location: str


@dataclass
class TemperatureRanges:
    maximum: float
    minimum: float


@dataclass
class ConnectorsConfiguration:
    kafka: Union[KafkaConfiguration, None] = None
    influxdb: Union[InfluxDBConfiguration, None] = None
    file_system: Union[FileSystemConfiguration, None] = None
    temperature_ranges: Union[TemperatureRanges, None] = None

    def enabled_configs(self) -> List:
        connectors_enabled = []
        for i in ['kafka', 'influxdb', 'file_system']:
            conn = getattr(self, i)
            if conn:
                connectors_enabled.append(conn)
        return connectors_enabled


# class Connectors:
#     def __init__(self, config: ConnectorsConfiguration):
#         self.config = config
#         self.kafka = None
#         self.influxdb = None
#         self.file_system = None


def load_config(filename=None,) -> ConnectorsConfiguration:
    if not filename:
        filename: Path = HOME / '.config' / CONFIG_FILE_NAME

    config = configparser.ConfigParser()
    config_file = Path(filename)
    connector_config = ConnectorsConfiguration()

    if config_file.is_file():
        config.read(filename)
    else:
        logger.warning('Unable to find config file.')
        return connector_config

    for section in config.keys():
        if section == 'kafka':
            connector_config.kafka = KafkaConfiguration(
                bootstrap_servers=config[section]['bootstrap_servers'],
                topics=config[section]['topics']
            )

        elif section == 'influxdb':
            connector_config.influxdb = InfluxDBConfiguration(
                url=config[section]['url'],
                token=config[section]['token'],
                org=config[section]['org'],
                bucket=config[section]['bucket'],
            )

        elif section == 'file_system':
            connector_config.file_system = FileSystemConfiguration(
                filename=config[section]['filename'],
            )

        elif section == 'temperature_ranges':
            connector_config.temperature_ranges = TemperatureRanges(
                maximum=float(config[section]['maximum']),
                minimum=float(config[section]['minimum']),
            )

        elif section == 'local':
            connector_config.local = LocalConfiguration(
                location=config[section]['location'],
            )

    return connector_config
