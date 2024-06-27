import pymongo
import json
import os
import glob

# Replace with your actual MongoDB connection details
connection_string = "mongodb+srv://pippo:HSBFjpCRp7sIH2p5@cluster0.hqsn7ul.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

try:
    # Connect to MongoDB
    client = pymongo.MongoClient(connection_string)
    db = client.MeteoAnalytics  # Replace with your database name
    collection = db.Inquinamento  # Replace with your collection name

    # Directory containing the JSON files
    json_directory = "C:\\Users\\USER\\Desktop\\sensori_puliti-20240627T164829Z-001\\sensori_puliti"

    # Iterate through all JSON files in the directory
    for filepath in glob.glob(os.path.join(json_directory, "*.json")):
        with open(filepath, "r") as f:
            data = json.load(f)

    #Check if the data is a list of documents or a single document
            if isinstance(data, list):
                collection.insert_many(data)
                print(f"Documents from {os.path.basename(filepath)} inserted successfully!")
            else:
                collection.insert_one(data)
                print(f"Document from {os.path.basename(filepath)} inserted successfully!")

except pymongo.errors.OperationFailure as e:
    print(f"Operation failure: {e}")
except Exception as e:
    print(f"An error occurred: {e}")