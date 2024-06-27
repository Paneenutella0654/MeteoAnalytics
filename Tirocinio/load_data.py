import os
import pymongo
import json

# Connessione al database MongoDB
client = pymongo.MongoClient("mongodb+srv://gerardofrino588:95VOEFttqh89tAsS@cluster0.fdg5slg.mongodb.net/DBMeteoAnalytics?retryWrites=true&w=majority")
db = client["MeteoAnalytics"]
collection = db["Sensori"]

# Caricamento del file JSON
with open("Tirocinio\sensor_35.899246312094625_14.5141040186575.json", "r") as f:
    data = json.load(f)

print(data)

#collection.insert_one(data)
