from jocasta.config import ConnectorsConfiguration
from jocasta.inputs.serial_connector import SerialSensor


class InputManager:
    def __init__(self, configs: ConnectorsConfiguration):
        self.config = configs
        self._arduino = None
        self._garden = None

    @property
    def arduino(self):
        if not self._arduino and self.configs.
