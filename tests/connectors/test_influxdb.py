from unittest.mock import MagicMock

from freezegun import freeze_time

from jocasta.connectors.influx import _build_payload, InfluxDBConnector

EXAMPLE_PAYLOAD = [
    {
        'measurement': 'light',
        'tags': {'host': 'WRLONMBP106.local', 'location': 'office'},
        'time': '2020-01-01T00:00:00',
        'fields': {'value': 100},
    },
    {
        'measurement': 'temperature',
        'tags': {'host': 'WRLONMBP106.local', 'location': 'office'},
        'time': '2020-01-01T00:00:00',
        'fields': {'value': 25.7},
    },
]
EXAMPLE_READING = {'light': 100, 'temperature': 25.7, 'location': 'office'}


@freeze_time('2020-01-01')
def test_build_payload():
    assert _build_payload(EXAMPLE_READING) == EXAMPLE_PAYLOAD


def test_connector():
    connector = InfluxDBConnector('db', 'pass', 'user')
    connector.influx_client = MagicMock()

    connector.send(EXAMPLE_READING)

    print(connector.influx_client.called)
