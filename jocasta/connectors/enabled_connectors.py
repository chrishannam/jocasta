from jocasta.config import ConnectorsConfiguration
from jocasta.config import KafkaConfiguration
from jocasta.connectors.kafka import KafkaConnector


class EnabledConnectors:
    def __init__(self, config: ConnectorsConfiguration):

        for conf in config.enabled_configs():
            if isinstance(conf, KafkaConfiguration):
                self.kafka = KafkaConnector(configuration=conf)
