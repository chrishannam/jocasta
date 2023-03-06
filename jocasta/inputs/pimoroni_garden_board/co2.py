from datetime import datetime

from pydantic import BaseModel
from scd4x import SCD4X


class CO2Reading(BaseModel):
    co2: int
    temperature: float
    humidity: float
    timestamp: datetime


class CO2Sensor:
    def __init__(self, quiet=True):
        self.device = SCD4X(quiet=quiet)
        self.device.start_periodic_measurement()

    def get_reading(self):
        co2, temperature, humidity, timestamp = self.device.measure()
        return CO2Reading(
            co2=co2,
            temperature=round(temperature, 2),
            humidity=round(humidity, 2),
            timestamp=datetime.utcfromtimestamp(timestamp)
        )
