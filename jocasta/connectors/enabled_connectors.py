from jocasta.config import ConnectorsConfiguration
from jocasta.config import FileSystemConfiguration
from jocasta.config import InfluxDBConfiguration
from jocasta.config import KafkaConfiguration
from jocasta.config import TapoConfiguration
from jocasta.connectors.file_system import FileSystemConnector
from jocasta.connectors.influxdb import InfluxDBConnector
from jocasta.connectors.kafka import KafkaConnector
from jocasta.connectors.tapo import TapoConnector


class EnabledConnectors:
    def __init__(self, config: ConnectorsConfiguration):
        self.connectors = []
        for conf in config.enabled_configs():
            if isinstance(conf, KafkaConfiguration):
                self.kafka = KafkaConnector(configuration=conf)
                self.connectors.append(self.kafka)
            elif isinstance(conf, InfluxDBConfiguration):
                self.influxdb = InfluxDBConnector(configuration=conf)
                self.connectors.append(self.influxdb)
            elif isinstance(conf, FileSystemConfiguration):
                self.file_system = FileSystemConnector(configuration=conf)
                self.connectors.append(self.file_system)
            elif isinstance(conf, TapoConfiguration):
                self.tapo = TapoConnector(configuration=conf)
                self.connectors.append(self.tapo)