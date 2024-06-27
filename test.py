import json
import requests

def get_air_quality(latitude, longitude):
    print("sto nel API")
    url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={latitude}&longitude={longitude}&hourly=pm10,pm2_5,carbon_monoxide&start_date=2022-12-01&end_date=2023-12-31"
    print(url)
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data for latitude {latitude} and longitude {longitude}: {response.status_code}")
        return None

def main(json_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    
    for indice, item in enumerate(data):
        if 'id' in item and 'lat' in item and 'lon' in item:
            latitude = item['lat']
            longitude = item['lon']
            air_quality_data = get_air_quality(latitude, longitude)
            if air_quality_data:
                nome_file = f'dati_{indice + 1}_2.json'
                with open(nome_file, 'w') as f:
                    json.dump(air_quality_data, f, indent=4)
                    print(f"Dati salvati in '{nome_file}'")
            else:
                print(f"Non è stato possibile ottenere i dati di qualità dell'aria per la latitudine {latitude} e longitudine {longitude}")

# Percorso del file JSON contenente id, latitude e longitude
json_file_path = 'coordinate.json'
main(json_file_path)