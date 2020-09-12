import tempfile
from pathlib import Path
from jocasta.connectors.csv_file import CSVFileConnector
import pytest
import csv

FILENAME = 'output.csv'


@pytest.fixture
def connector():
    return CSVFileConnector(FILENAME)


def test_connector(reading):
    with tempfile.TemporaryDirectory() as tmp_dir_name:
        tmp_dir_name_path = Path(tmp_dir_name)
        csv_output_file = tmp_dir_name_path / FILENAME
        connector = CSVFileConnector(csv_output_file)
        connector.send(reading)
        assert _test_csv_file(csv_output_file, reading)


def _test_csv_file(filename, reading):
    with open(filename, newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        csv_data = list(reader)
        return csv_data[0].keys() == reading.keys()
