from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
import json



if __name__ == "__main__":
    owm = OWM('b0f7c64a5f517f0d157b6a5a9c720157')
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place('Beverley,GB')
    w = observation.weather

    with open('/tmp/weather.json', 'w') as filename:
        json.dump(w.temperature('celsius'), filename, indent=4)

