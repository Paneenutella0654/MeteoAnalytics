import os
import json
from datetime import datetime

def remove_data(data):

    keys_to_remove = [
        "pressure_msl",
        "wind_speed_100m",
        "wind_direction_100m",
        "direct_radiation_instant",
        "direct_normal_irradiance_instant",
        "nitrogen_dioxide",
        "ozone",
        "ammonia"
    ]
    
    for measurement in data["measurements"]:
        for key in keys_to_remove:
            if key in measurement:
                del measurement[key]
    return data

def filter_measurements_by_time(measurements, desired_times):
    filtered = []
    for measurement in measurements:
        time = measurement['time'][11:16]  # Estrai l'ora dal timestamp
        if time in desired_times:
            filtered.append(measurement)
    return filtered

def filter_measurements_by_date(measurements, cutoff_date):

    cutoff_datetime = datetime.strptime(cutoff_date, '%Y-%m-%d')
    filtered = []
    for measurement in measurements:
        measurement_date = datetime.strptime(measurement['time'][:10], '%Y-%m-%d')
        if measurement_date >= cutoff_datetime:
            filtered.append(measurement)
    return filtered

def process_files(input_folder, output_folder, desired_times, cutoff_date):

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".json"):
            file_path = os.path.join(input_folder, filename)

            with open(file_path, 'r') as f:
                data = json.load(f)

            data['measurements'] = filter_measurements_by_date(data['measurements'], cutoff_date)


            data['measurements'] = filter_measurements_by_time(data['measurements'], desired_times)

            data = remove_data(data)

            output_file_path = os.path.join(output_folder, filename)
            with open(output_file_path, 'w') as f:
                json.dump(data, f, indent=4)

            print(f"File elaborato e salvato come {output_file_path}")


input_folder = "/content/drive/Shareddrives/sensori"  
output_folder = "/content/Sensori_aggiustati"  
desired_times = ["03:00", "12:00", "21:00"]  
cutoff_date = "2015-01-01"  


process_files(input_folder, output_folder, desired_times, cutoff_date)
