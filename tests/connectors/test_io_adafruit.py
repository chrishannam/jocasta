from unittest.mock import MagicMock
import pytest
from jocasta.connectors.io_adafruit import IOAdafruitConnector


@pytest.fixture
def measurements():
    return 'office.office-temperature,office.office-light,office.office-humidity'


def test_connector(measurements, reading):
    connector = IOAdafruitConnector(
        'key',
        'username',
        'office.office-temperature,office.office-light,office.office-humidity',
        'temperature,light,humidity',
    )

    connector.aio = MagicMock()
    connector.send(reading)

    assert connector.aio.send_data.called
