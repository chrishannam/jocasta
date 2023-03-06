import json
from dataclasses import dataclass
from typing import Dict


@dataclass
class FileSystemConfiguration:
    filename: str


class FileSystemConnector:
    def __init__(self, configuration: FileSystemConfiguration):
        self.file_name = configuration.filename

    def send(self, readings, hostname: str, location: str) -> bool:
        """
        Write data as JSON to file.
        """

        with open(self.file_name, 'w') as f:
            output = readings.to_dict()
            output['arduino'] = output['arduino'].dict()
            f.write(json.dumps(output, indent=4))

        return True
