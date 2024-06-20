from bson.objectid import ObjectId
from typing import List

class sensore():
   def __init__(self, id, name, box_type, exposure, model, propietario, loc, sensors):
        self.id = id
        self.name = name
        self.box_type = box_type
        self.exposure = exposure
        self.model = model
        self.propietario = propietario
        self.loc = {"geometry": {"coordinates": loc.get("geometry", {}).get("coordinates", []), "type": "Point"}}
        self.sensors = [
            {
                "title": sensor["title"],
                "unit": sensor["unit"],
                "sensor_type": sensor["sensorType"],
                "id": sensor["id"]
            }
            for sensor in sensors
        ]
