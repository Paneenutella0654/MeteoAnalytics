# La tua lista di sensoritutti
sensoritutti = {
  "sensors": [
    {
      "title": "Luminosità",
      "unit": "Pegel",
      "sensorType": "GL5528",
      "id": "538da4d6a834155415765eaf"
    },
    {
      "title": "Anemometro",
      "unit": "m/s",
      "sensorType": "KWG1",
      "id": "538da4d6a834155415765eb0"
    },
    {
      "title": "ATM Aria",
      "unit": "Pa",
      "sensorType": "BMP085",
      "id": "538da4d6a834155415765eb1"
    },
    {
      "title": "Umidità",
      "unit": "%",
      "sensorType": "DHT11",
      "id": "538da4d6a834155415765eb2"
    },
    {
      "title": "Temperatura",
      "unit": "°C",
      "sensorType": "BMP085",
      "id": "538da4h8b334155415765eb3"
    },
    {
      "title": "Inquinamento",
      "unit": "μg/m³",
      "sensorType": "MQ-2",
      "id": "538da4d6a216855415765db6"
    },
    {
      "title": "Precipitazioni",
      "unit": "mm",
      "sensorType": "S-RGB-M002",
      "id": "538da4d6g5912355415765dg6"
    }
  ]
}


from src.help_functions import sensoritutti

def creadict(sensori_richiesta):
    nuovo_lista = [
        {"title": sensore["title"],
         "unit": sensore["unit"],
         "sensorType": sensore["sensorType"],
         "id": sensore["id"]
        }
        for sensore in sensoritutti["sensors"] if sensore["title"] in sensori_richiesta
    ]
    return nuovo_lista