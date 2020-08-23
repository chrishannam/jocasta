from jocasta.collector import setup_connectors
from jocasta.command_line.setup import setup_config

from pathlib import Path

from jocasta.connectors.file_system import FileSystemConnector
from jocasta.connectors.influx import InfluxDBConnector
from jocasta.connectors.io_adafruit import IOAdafruitConnector

INI_FILE = Path(__file__).parent / '..' / 'jocasta_config.ini.example'

ENABLED_CONNECTORS = {
    'file_system': FileSystemConnector,
    'io_adafruit': IOAdafruitConnector,
    'influxdb': InfluxDBConnector,
}


def test_setup_connectors():
    config = setup_config(ini_file=INI_FILE)
    connectors = setup_connectors(config)

    for name, connector in ENABLED_CONNECTORS.items():
        assert isinstance(connectors[name], connector)
