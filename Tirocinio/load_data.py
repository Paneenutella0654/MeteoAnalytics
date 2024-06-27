import os
import pymongo
import json

# Connessione al database MongoDB
client = pymongo.MongoClient("mongodb+srv://gerardofrino588:HFP1WMfpsjD1cfDA@cluster0.fdg5slg.mongodb.net/DBMeteoAnalytics?retryWrites=true&w=majority")
db = client["MeteoAnalytics"]
collection = db["Inquinamento"]

# Percorso della cartella contenente i file JSON da caricare
folder_path = "sensori_puliti"

# Ciclo attraverso tutti i file nella cartella specificata
for filename in os.listdir(folder_path):
    if filename.endswith(".json"):
        file_path = os.path.join(folder_path, filename)

        # Caricamento del file JSON
        with open(file_path, "r") as f:
            data = json.load(f)

        # Inserire i dati in MongoDB
        collection.insert_one(data)
        print(f"Dati da '{filename}' inseriti in MongoDB.")

client.close()
