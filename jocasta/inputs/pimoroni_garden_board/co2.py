from datetime import datetime

from scd4x import SCD4X
from dataclasses import dataclass


@dataclass
class CO2Reading:
    co2: int
    temperature: float
    humidity: float
    timestamp: datetime


class CO2Sensor:
    def __init__(self, quiet=True):
        self.device = SCD4X(quiet=quiet)
        self.device.start_periodic_measurement()

    def reading(self):
        co2, temperature, humidity, timestamp = self.device.measure()
        return CO2Reading(
            co2=co2,
            temperature=round(temperature, 2),
            humidity=round(humidity, 2),
            timestamp=datetime.utcfromtimestamp(timestamp)
        )
