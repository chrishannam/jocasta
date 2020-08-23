import pytest


@pytest.fixture
def hostname():
    return 'WR01.local'


@pytest.fixture
def payload(hostname):
    return [
        {
            'measurement': 'light',
            'tags': {'host': hostname, 'location': 'office'},
            'fields': {'value': 100.0},
        },
        {
            'measurement': 'temperature',
            'tags': {'host': hostname, 'location': 'office'},
            'fields': {'value': 25.7},
        },
        {
            'measurement': 'humidity',
            'tags': {'host': hostname, 'location': 'office'},
            'fields': {'value': 50.0},
        },
    ]


@pytest.fixture
def reading():
    return {'light': 100.0, 'temperature': 25.7, 'humidity': 50.0, 'location': 'office'}
