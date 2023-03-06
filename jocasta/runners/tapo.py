"""
Office etc
"""

from jocasta.config import load_config
from jocasta.outputs.enabled_connectors import EnabledConnectors


def main():
    configs = load_config()
    connectors = EnabledConnectors(configs)

    data = connectors.tapo.fetch()

    for name, data in data.items():
        connectors.influxdb.send_tapo(data=data, name=name)


if __name__ == '__main__':
    main()
