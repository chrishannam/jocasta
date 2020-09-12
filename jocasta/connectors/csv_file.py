import csv
import pathlib
import logging


logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

logger = logging.getLogger(__name__)


class CSVFileConnector(object):
    def __init__(self, path):

        self.file_path = path

    def send(self, data) -> bool:
        write_header = False

        # check for file
        path = pathlib.Path(self.file_path)

        if not path.exists():
            write_header = True

        with open(self.file_path, 'a') as csv_file:
            fieldnames = data.keys()
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            # if we have a new file, write the header
            if write_header:
                writer.writeheader()
            writer.writerow(data)
        return True
