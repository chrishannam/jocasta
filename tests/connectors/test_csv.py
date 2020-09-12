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
        assert _test_csv_file(tmp_dir_name_path, reading)


def _test_csv_file(filename, reading):
    csv_data = []
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            csv_data.append(row)
    assert csv_data == reading
