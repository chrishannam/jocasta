"""
Office etc
"""
from typing import Dict

from tapo_plug import tapoPlugApi
import json

from jocasta.collector import setup_connectors
from jocasta.command_line.setup import setup_config


def main():
    config = setup_config(ini_file=None)

    if not config.has_section('tapo_plugs'):
        print('No Tapo config in your config file, see README.md')

    email = config.get('tapo_plugs', 'email')
    password = config.get('tapo_plugs', 'password')
    addresses = config.get('tapo_plugs', 'ipaddresses').split(',')

    connectors: Dict = setup_connectors(config=config)

    for address in addresses:
        device_name = address.split(':')[0]
        ip = address.split(':')[1]
        device = {
            'tapoEmail': email,
            'tapoPassword': password,
            'tapoIp': ip
        }
        result = tapoPlugApi.getPlugUsage(device)
        data = json.loads(result)

        for name, reading in data['result'].items():
            connectors['influxdb'].send_tapo(section=name, data=reading, device_name=device_name)


if __name__ == '__main__':
    main()
# response = tapoPlugApi.getDeviceInfo(device)
#response = tapoPlugApi.getPlugUsage(device)