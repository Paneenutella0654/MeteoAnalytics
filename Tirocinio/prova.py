import os
import json

def remove_data(data):

    cose_eliminare = [
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
        for key in cose_eliminare:
            if key in measurement:
                del measurement[key]
    return data

def filto(measurements, desired_times):

    filtered = []
    for measurement in measurements:
        time = measurement['time'][11:16]  
        if time in desired_times:
            filtered.append(measurement)
    return filtered

def process_files(input_folder, output_folder, ore_da_prendere):

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".json"):
            file_path = os.path.join(input_folder, filename)

            with open(file_path, 'r') as f:
                data = json.load(f)

            data = remove_data(data)
            data['measurements'] = filto(data['measurements'], ore_da_prendere)
            output_file_path = os.path.join(output_folder, filename)
            with open(output_file_path, 'w') as f:
                json.dump(data, f, indent=4)



input_folder = "/content/drive/Shareddrives/sensori"  
output_folder = "/content/Sensori_aggiustati"  
ore_da_prendere = ["00:00" "12:00"]  

process_files(input_folder, output_folder, ore_da_prendere)
