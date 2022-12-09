from unittest.mock import MagicMock
from deepdiff import DeepDiff
from jocasta.connectors.influxdb import _build_payload, InfluxDBConnector


def test_build_payload(reading, payload, hostname):

    output = _build_payload(reading, hostname=hostname)
    assert not DeepDiff(payload, output, ignore_order=True)


def test_connector(reading, payload, hostname):
    connector = InfluxDBConnector('db', 'pass', 'user')
    connector.influx_client = MagicMock()
    connector.send(reading, hostname=hostname)
    connector.influx_client.write_points.assert_called_with(payload)
