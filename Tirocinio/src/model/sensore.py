from bson.objectid import ObjectId
from typing import List

class sensore():
    def __init__(self, id, latitude, longitude,measurements):
        self.id = id
        self.loc = {"geometry": {"coordinates": [longitude, latitude], "type": "Point"}}
        self.measurements = [
            {
                "time": measurement["time"],
                "temperature_2m": measurement.get("temperature_2m"),
                "relative_humidity_2m": measurement.get("relative_humidity_2m"),
                "precipitation": measurement.get("precipitation"),
                "rain": measurement.get("rain"),
                "snowfall": measurement.get("snowfall"),
                "surface_pressure": measurement.get("surface_pressure"),
                "wind_speed_10m": measurement.get("wind_speed_10m"),
                "wind_direction_10m": measurement.get("wind_direction_10m"),
                "wind_gusts_10m": measurement.get("wind_gusts_10m"),
                "soil_temperature_0_to_7cm": measurement.get("soil_temperature_0_to_7cm"),
                "direct_radiation": measurement.get("direct_radiation"),
                "pm10": measurement.get("pm10"),
                "pm2_5": measurement.get("pm2_5"),
                "carbon_monoxide": measurement.get("carbon_monoxide")
            }
            for measurement in measurements
        ]
