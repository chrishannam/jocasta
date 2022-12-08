import json
from typing import Dict

from jocasta.config import FileSystemConfiguration


class FileSystemConnector:
    def __init__(self, configuration: FileSystemConfiguration):
        self.file_name = configuration.filename

    def send(self, data: Dict) -> bool:
        """
        Write data as JSON to file.
        """

        with open(self.file_name, 'w') as f:
            f.write(json.dumps(data))

        return True
