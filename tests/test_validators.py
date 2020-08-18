from jocasta.validators import validate_temperature

import pytest


@pytest.mark.parametrize(
    "reading, value_range, valid",
    [
        ({'temperature': -127.0, 'light': 100}, {'maximum': 50, 'minimum': -5}, False),
        ({'temperature': 27.0, 'light': 100}, {'maximum': 50, 'minimum': -5}, True),
        ({'temperature': 75.0, 'light': 100}, {'maximum': 50, 'minimum': -5}, False),
    ],
)
def test_validate_temperature(reading, value_range, valid):
    if not valid:
        del reading['temperature']

    assert validate_temperature(reading, value_range) == reading
