import os
import json
from datetime import datetime

def remove_params(json_data):
    # Parametri da rimuovere
    params_to_remove = [
        "generationtime_ms",
        "utc_offset_seconds",
        "timezone",
        "timezone_abbreviation",
        "elevation",
        "hourly_units"
    ]

    # Rimuovi i parametri dal dizionario principale
    for param in params_to_remove:
        if param in json_data:
            del json_data[param]

    return json_data

def filter_measurements(json_data):
    hourly_data = json_data.get("hourly", {})

    if not hourly_data:
        return json_data

    time_data = hourly_data.get("time", [])
    pm10_data = hourly_data.get("pm10", [])
    pm2_5_data = hourly_data.get("pm2_5", [])
    co_data = hourly_data.get("carbon_monoxide", [])

    filtered_time = []
    filtered_pm10 = []
    filtered_pm2_5 = []
    filtered_co = []

    for idx, time in enumerate(time_data):
        if time.endswith("03:00") or time.endswith("12:00") or time.endswith("21:00"):
            filtered_time.append(time)
            filtered_pm10.append(pm10_data[idx])
            filtered_pm2_5.append(pm2_5_data[idx])
            filtered_co.append(co_data[idx])

    hourly_data["time"] = filtered_time
    hourly_data["pm10"] = filtered_pm10
    hourly_data["pm2_5"] = filtered_pm2_5
    hourly_data["carbon_monoxide"] = filtered_co

    return json_data

def process_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('.json'):
            input_file_path = os.path.join(input_folder, filename)
            output_file_path = os.path.join(output_folder, filename)

            with open(input_file_path, 'r') as file:
                json_data = json.load(file)

            json_data = remove_params(json_data)
            json_data = filter_measurements(json_data)

            with open(output_file_path, 'w') as outfile:
                json.dump(json_data, outfile, indent=4)

            print(f"File '{filename}' elaborato e salvato in '{output_folder}'.")

# Esempio di utilizzo
if __name__ == "__main__":
    # Specifica la cartella di input e di output
    input_folder = 'Inquinamento'
    output_folder = 'sensori_puliti'

    # Esegui il processo per la cartella di input
    process_folder(input_folder, output_folder)
