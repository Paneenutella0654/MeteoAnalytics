import hashlib , re, datetime
from src.dbConnection import  utenti,sensori,coordinate, inquinamento, coordinate_n
"from src import login_manager"
from src.model.utente import utente
from src.model.sensore import sensore
from bson.objectid import ObjectId
from flask import request, render_template, session, jsonify, redirect
from src import app
from flask_login import current_user, login_required
from datetime import datetime, timedelta

def UtentebyID (id : str) -> utente:
    trovato = utenti.find_one({"_id": ObjectId(id)})
    if trovato is None:
        return None
    id = str(trovato.get("_id"))
    nome = trovato.get("nome")
    cognome = trovato.get("cognome")
    email = trovato.get("email")
    ruolo = trovato.get("ruolo")
    password = trovato.get("password")
    utenteTrovato = utente(id,email,password,nome,cognome,ruolo)
    return utenteTrovato

def UtentebyEmail (email:str) -> utente :
    trovato = utenti.find_one({"email": email})
    if trovato is None:
        return None
    id = str(trovato.get("_id"))
    nome = trovato.get("nome")
    cognome = trovato.get("cognome")
    email = trovato.get("email")
    ruolo = trovato.get("ruolo")
    password = trovato.get("password")
    utenteTrovato = utente(id,email,password,nome,cognome,ruolo)
    return utenteTrovato

def RetriveUtenti(ruolot):
    if ruolot != "admin":
        trovati = utenti.find({"ruolo": {"$ne": "admin"}})
    elif ruolot == "admin":
        trovati = utenti.find()
    listaUtenti = []
    for trovato in trovati:
        id = str(trovato.get("_id"))
        nome = trovato.get("nome")
        cognome = trovato.get("cognome")
        email = trovato.get("email")
        ruolo = trovato.get("ruolo")
        password = trovato.get("password")
        new_Utente = utente(id,email,password,nome,cognome,ruolo)
        listaUtenti.append(new_Utente)
    return listaUtenti

def creaUtente(nome: str, cognome: str, email: str, password: str, ruolo: str):
          result = utenti.insert_one({"nome":nome,"cognome":cognome,"email":email,"password":password,"ruolo":ruolo})
          return result
      

def Retrive_one_Sensori(id : str) -> sensore:
    trovato = sensori.find_one({"_id": ObjectId(id)})
    listaSensori = []
    id2 = str(trovato.get("_id"))
    latitude = trovato.get("latitude")
    longitude = trovato.get("longitude")
    measurements = []
    if "measurements" in trovato:
        measurements = [
            {
                "time": m["time"],
                "temperature_2m": m.get("temperature_2m"),
                "relative_humidity_2m": m.get("relative_humidity_2m"),
                "precipitation": m.get("precipitation"),
                "rain": m.get("rain"),
                "snowfall": m.get("snowfall"),
                "surface_pressure": m.get("surface_pressure"),
                "wind_speed_10m": m.get("wind_speed_10m"),
                "wind_direction_10m": m.get("wind_direction_10m"),
                "wind_gusts_10m": m.get("wind_gusts_10m"),
                "soil_temperature_0_to_7cm": m.get("soil_temperature_0_to_7cm"),
                "direct_radiation": m.get("direct_radiation"),
                "pm10": m.get("pm10"),
                "pm2_5": m.get("pm2_5"),
                "carbon_monoxide": m.get("carbon_monoxide")
            }
            for m in trovato["measurements"]
        ]
    else:
        print(f"Il documento con _id {id2} non contiene 'measurements'")
    
    listaSensori.append({
        "id": id2,
        "latitude": latitude,
        "longitude": longitude,
        "measurements": measurements
    })
    return listaSensori

def SensorebyID (id : str) -> sensore:
    trovato = sensori.find_one({"_id": ObjectId(id)})
    if trovato is None:
        return None
    Sensore = []
    id2 = str(trovato.get("_id"))
    latitude = trovato.get("latitude")
    longitude = trovato.get("longitude")
    measurementsPrecipitation = [
         {
              "time": m["time"],
              "relative_humidity_2m": m.get("relative_humidity_2m"),
              "precipitation": m.get("precipitation"),
              "rain": m.get("rain"),
              "snowfall": m.get("snowfall"),
         }
            for m in trovato["measurements"]
    ]
    measurementsWind = [
         {
              "time": m["time"],
              "wind_speed_10m": m.get("wind_speed_10m"),
              "wind_direction_10m": m.get("wind_direction_10m"),
              "wind_gusts_10m": m.get("wind_gusts_10m"),
         }
            for m in trovato["measurements"]
    ]
    measurementsTemperature = [
         {
              "time": m["time"],
              "temperature_2m": m.get("temperature_2m"),
              "soil_temperature_0_to_7cm": m.get("soil_temperature_0_to_7cm"),
              "surface_pressure": m.get("surface_pressure"),
              "direct_radiation": m.get("direct_radiation"),
         }
            for m in trovato["measurements"]
    ]
    
    Sensore.append({
            "id": id2,
            "latitude": latitude,
            "longitude": longitude,
            "measurementsPrecipitation": measurementsPrecipitation,
            "measurementsWind": measurementsWind,
            "measurementsTemperature": measurementsTemperature
        })
    return Sensore

def AggiungiSensore(name: str, box_type: str, exposure: str, model: str, propietario: str, loc: dict, sensors: dict):
    result = sensori.insert_one({"name":name,"box_type":box_type,"exposure":exposure,"model":model,"propietario":propietario,"loc":loc,"sensors":sensors})
    return result
      
def EliminaSensore(id: str):
    result = coordinate.delete_one({"id": id})
    return result
      
def ModificaSensore(id: str, name: str, box_type: str, exposure: str, model: str, propietario: str, loc: dict, sensors: dict):
    result = sensori.update_one({"_id": ObjectId(id)},{"$set":{"name":name,"box_type":box_type,"exposure":exposure,"model":model,"propietario":propietario,"loc":loc,"sensors":sensors}})
    return result

def creaUtente(nome: str, cognome: str, email: str, password: str):
          result = utenti.insert_one({"nome":nome,"cognome":cognome,"password":password,"email":email})
          return result
      
def RetriveCoordinareSensori():
    trovati = coordinate_n.find()
    listaCoordinate = []
    for trovato in trovati:
        id = str(trovato.get("id"))
        latitude = trovato.get("lat")
        longitude = trovato.get("lon")
        nazione = trovato.get("nazione")
        
        listaCoordinate.append({
            "id": id,
            "lat": latitude,
            "lon": longitude,
            "nazione": nazione
        })
    return listaCoordinate

def RetriveInquinamentoBySensoredID(id:str):
    trovato = inquinamento.find_one({"id": id})
    inquinamentoTrovato = []
    if trovato is None:
        return None
    id = str(trovato.get("_id"))
    idSensore = trovato.get("id")
    hourly = trovato.get("hourly")
    time = hourly.get("time")
    pm10 = hourly.get("pm10")
    pm2_5 = hourly.get("pm2_5")
    carbon_monoxide = hourly.get("carbon_monoxide")
    inquinamentoTrovato.append({
        "id": id,
        "idSensore": idSensore,
        "time": time,
        "pm10": pm10,
        "pm2_5": pm2_5,
        "carbon_monoxide": carbon_monoxide
    })
    return inquinamentoTrovato

def sensoriByNazione(nazione: str):
    trovati = coordinate_n.find({"nazione": nazione})
    listaCoordinate = []
    for trovato in trovati:
        id = str(trovato.get("id"))
        latitude = trovato.get("lat")
        longitude = trovato.get("lon")
        nazione = trovato.get("nazione")

        listaCoordinate.append({
            "id": id,
            "lat": latitude,
            "lon": longitude,
            "nazione": nazione
        })
    return listaCoordinate

# Query per il recupero dei dati di un sensore in una data sepcifca
def Filter_by_date(id: str, data: str) -> sensore:
    # Converte la data in oggetto datetime
    date_obj = datetime.strptime(data, "%Y-%m-%dT%H:%M:%S")
    
    # Calcola l'inizio e la fine del giorno
    start_of_day = date_obj.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=1)

    # Costruzione della query
    query = {
        "_id": ObjectId(id),
        "measurements": {
            "$elemMatch": {
                "time": {
                    "$gte": start_of_day.strftime("%Y-%m-%dT%H:%M:%S"),
                    "$lt": end_of_day.strftime("%Y-%m-%dT%H:%M:%S")
                }
            }
        }
    }

    # Proiezione per includere solo le misurazioni del giorno specificato
    projection = {
        "latitude": 1,
        "longitude": 1,
        "measurements": {
            "$filter": {
                "input": "$measurements",
                "as": "m",
                "cond": {
                    "$and": [
                        {"$gte": ["$$m.time", start_of_day.strftime("%Y-%m-%dT%H:%M:%S")]},
                        {"$lt": ["$$m.time", end_of_day.strftime("%Y-%m-%dT%H:%M:%S")]}
                    ]
                }
            }
        }
    }
    
    trovato = sensori.find_one(query, projection)
    if trovato is None:
        return None

    Sensorebydate = []
    measurementsPrecipitation = [
        {
            "time": m["time"],
            "relative_humidity_2m": m.get("relative_humidity_2m"),
            "precipitation": m.get("precipitation"),
            "rain": m.get("rain"),
            "snowfall": m.get("snowfall"),
        }
        for m in trovato["measurements"]
    ]
    measurementsWind = [
        {
            "time": m["time"],
            "wind_speed_10m": m.get("wind_speed_10m"),
            "wind_direction_10m": m.get("wind_direction_10m"),
            "wind_gusts_10m": m.get("wind_gusts_10m"),
        }
        for m in trovato["measurements"]
    ]
    measurementsTemperature = [
        {
            "time": m["time"],
            "temperature_2m": m.get("temperature_2m"),
            "soil_temperature_0_to_7cm": m.get("soil_temperature_0_to_7cm"),
            "surface_pressure": m.get("surface_pressure"),
            "direct_radiation": m.get("direct_radiation"),
        }
        for m in trovato["measurements"]
    ]

    Sensorebydate.append({
        "id": id,
        "latitude": trovato.get("latitude"),
        "longitude": trovato.get("longitude"),
        "measurementsPrecipitation": measurementsPrecipitation,
        "measurementsWind": measurementsWind,
        "measurementsTemperature": measurementsTemperature
    })

    return Sensorebydate

def Filter_inquinamento_by_date(id: str, data: str):
    # Converte la data in oggetto datetime
    date_obj = datetime.strptime(data, "%Y-%m-%dT%H:%M")
    
    # Calcola l'inizio e la fine del giorno
    start_of_day = date_obj.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=1)

    # Costruzione della query
    query = {
        "id": id,
        "hourly.time": {
            "$gte": start_of_day.strftime("%Y-%m-%dT%H:%M"),
            "$lt": end_of_day.strftime("%Y-%m-%dT%H:%M")
        }
    }

    # Proiezione per includere solo i campi necessari
    projection = {
        "latitude": 1,
        "longitude": 1,
        "hourly.time": 1,
        "hourly.carbon_monoxide": 1,
        "hourly.pm2_5": 1,
        "hourly.pm10": 1
    }
    
    trovato = inquinamento.find_one(query, projection)
    if trovato is None:
        return None

    InquinamentoByDate = []
    carbon_monoxide = []
    pm2_5 = []
    pm10 = []
    time2 = []
    

    # Assumiamo che 'hourly' sia un oggetto con array per ogni tipo di misurazione
    times = trovato["hourly"]["time"]
    for i, time in enumerate(times):
        if start_of_day <= datetime.strptime(time, "%Y-%m-%dT%H:%M") < end_of_day:
            time2.append(time)
            carbon_monoxide.append(trovato["hourly"]["carbon_monoxide"][i])
            pm2_5.append(trovato["hourly"]["pm2_5"][i])
            pm10.append(trovato["hourly"]["pm10"][i])

    InquinamentoByDate.append({
        "id": id,
        "latitude": trovato.get("latitude"),
        "longitude": trovato.get("longitude"),
        "time": time2, 
        "carbon_monoxide": carbon_monoxide,
        "pm2_5": pm2_5,
        "pm10": pm10
    })

    return InquinamentoByDate


# Query per il recupero di tutti i dati di un sensore da una data in poi
def Filter_by_date_gt (id: str, data: str) -> sensore:
 # Costruzione della query
    query = {
        "_id": ObjectId(id),
        "measurements": {
            "$elemMatch": {
                "time": data
            }
        }
    }

    # Proiezione per includere solo le misurazioni che soddisfano il criterio di data
    projection = {
        "latitude": 1,
        "longitude": 1,
        "measurements": {
            "$filter": {
                "input": "$measurements",
                "as": "m",
                "cond": {"$gt": ["$$m.time", data]}
            }
        }
    }
    
    trovato = sensori.find_one(query, projection)
    if trovato is None:
        return None
    Sensorebydategt = []
    measurementsPrecipitation = [
         {
              "time": m["time"],
              "relative_humidity_2m": m.get("relative_humidity_2m"),
              "precipitation": m.get("precipitation"),
              "rain": m.get("rain"),
              "snowfall": m.get("snowfall"),
         }
            for m in trovato["measurements"]
    ]
    measurementsWind = [
         {
              "time": m["time"],
              "wind_speed_10m": m.get("wind_speed_10m"),
              "wind_direction_10m": m.get("wind_direction_10m"),
              "wind_gusts_10m": m.get("wind_gusts_10m"),
         }
            for m in trovato["measurements"]
    ]
    measurementsTemperature = [
         {
              "time": m["time"],
              "temperature_2m": m.get("temperature_2m"),
              "soil_temperature_0_to_7cm": m.get("soil_temperature_0_to_7cm"),
              "surface_pressure": m.get("surface_pressure"),
              "direct_radiation": m.get("direct_radiation"),
         }
            for m in trovato["measurements"]
    ]

    Sensorebydategt.append({
        "id": id,
        "latitude": trovato.get("latitude"),
        "longitude": trovato.get("longitude"),
        "measurementsPrecipitation": measurementsPrecipitation,
        "measurementsWind": measurementsWind,
        "measurementsTemperature": measurementsTemperature
    })

    return Sensorebydategt

def Filter_inquinamento_by_date_gt(id: str, data: str):
    # Converte la data in oggetto datetime
    date_obj = datetime.strptime(data, "%Y-%m-%dT%H:%M")
    
    # Calcola l'inizio e la fine del giorno
    start_of_day = date_obj.replace(hour=0, minute=0, second=0, microsecond=0)

    # Costruzione della query
    query = {
        "id": id,
        "hourly.time": {
            "$gt": start_of_day.strftime("%Y-%m-%dT%H:%M")
        }
    }

    # Proiezione per includere solo i campi necessari
    projection = {
        "latitude": 1,
        "longitude": 1,
        "hourly.time": 1,
        "hourly.carbon_monoxide": 1,
        "hourly.pm2_5": 1,
        "hourly.pm10": 1
    }
    
    trovato = inquinamento.find_one(query, projection)
    if trovato is None:
        return None

    InquinamentoByDate = []
    carbon_monoxide = []
    pm2_5 = []
    pm10 = []
    time2 = []
    

    # Assumiamo che 'hourly' sia un oggetto con array per ogni tipo di misurazione
    times = trovato["hourly"]["time"]
    for i, time in enumerate(times):
        if start_of_day <= datetime.strptime(time, "%Y-%m-%dT%H:%M"):
            time2.append(time)
            carbon_monoxide.append(trovato["hourly"]["carbon_monoxide"][i])
            pm2_5.append(trovato["hourly"]["pm2_5"][i])
            pm10.append(trovato["hourly"]["pm10"][i])

    InquinamentoByDate.append({
        "id": id,
        "latitude": trovato.get("latitude"),
        "longitude": trovato.get("longitude"),
        "time": time2, 
        "carbon_monoxide": carbon_monoxide,
        "pm2_5": pm2_5,
        "pm10": pm10
    })

    return InquinamentoByDate

def Filter_by_date_range(id: str, start_date: str, end_date: str) -> list:
    # Costruzione della query
    query = {
        "_id": ObjectId(id),
        "measurements": {
            "$elemMatch": {
                "time": {
                    "$gte": start_date,
                    "$lte": end_date
                }
            }
        }
    }

    # Proiezione per includere solo le misurazioni che soddisfano il criterio di data
    projection = {
        "latitude": 1,
        "longitude": 1,
        "measurements": {
            "$filter": {
                "input": "$measurements",
                "as": "m",
                "cond": {
                    "$and": [
                        {"$gte": ["$$m.time", start_date]},
                        {"$lte": ["$$m.time", end_date]}
                    ]
                }
            }
        }
    }
    
    trovato = sensori.find_one(query, projection)
    if trovato is None:
        return None

    Sensorebydate = []
    measurementsPrecipitation = [
        {
            "time": m["time"],
            "relative_humidity_2m": m.get("relative_humidity_2m"),
            "precipitation": m.get("precipitation"),
            "rain": m.get("rain"),
            "snowfall": m.get("snowfall"),
        }
        for m in trovato["measurements"]
    ]
    measurementsWind = [
        {
            "time": m["time"],
            "wind_speed_10m": m.get("wind_speed_10m"),
            "wind_direction_10m": m.get("wind_direction_10m"),
            "wind_gusts_10m": m.get("wind_gusts_10m"),
        }
        for m in trovato["measurements"]
    ]
    measurementsTemperature = [
        {
            "time": m["time"],
            "temperature_2m": m.get("temperature_2m"),
            "soil_temperature_0_to_7cm": m.get("soil_temperature_0_to_7cm"),
            "surface_pressure": m.get("surface_pressure"),
            "direct_radiation": m.get("direct_radiation"),
        }
        for m in trovato["measurements"]
    ]

    Sensorebydate.append({
        "id": id,
        "latitude": trovato.get("latitude"),
        "longitude": trovato.get("longitude"),
        "measurementsPrecipitation": measurementsPrecipitation,
        "measurementsWind": measurementsWind,
        "measurementsTemperature": measurementsTemperature
    })

    return Sensorebydate

def Filter_inquinamento_by_date_range(id: str, data: str,end_date: str) :
    # Converte la data in oggetto datetime
    date_obj_1 = datetime.strptime(data, "%Y-%m-%dT%H:%M")
    end_day = datetime.strptime(end_date, "%Y-%m-%dT%H:%M")
    
    # Calcola l'inizio e la fine del giorno
    start_of_day = date_obj_1.replace(hour=0, minute=0, second=0, microsecond=0)

    # Costruzione della query
    query = {
        "id": id,
        "hourly.time": {
            "$gte": data,
            "$lte": end_date
        }
    }

    # Proiezione per includere solo i campi necessari
    projection = {
        "latitude": 1,
        "longitude": 1,
        "hourly.time": 1,
        "hourly.carbon_monoxide": 1,
        "hourly.pm2_5": 1,
        "hourly.pm10": 1
    }
    
    trovato = inquinamento.find_one(query, projection)
    if trovato is None:
        return None

    InquinamentoByDate = []
    carbon_monoxide = []
    pm2_5 = []
    pm10 = []
    time2 = []
    
    # Assumiamo che 'hourly' sia un oggetto con array per ogni tipo di misurazione
    times = trovato["hourly"]["time"]
    for i, time in enumerate(times):
        if start_of_day <= datetime.strptime(time, "%Y-%m-%dT%H:%M") < end_day:
            time2.append(time)
            carbon_monoxide.append(trovato["hourly"]["carbon_monoxide"][i])
            pm2_5.append(trovato["hourly"]["pm2_5"][i])
            pm10.append(trovato["hourly"]["pm10"][i])

    InquinamentoByDate.append({
        "id": id,
        "latitude": trovato.get("latitude"),
        "longitude": trovato.get("longitude"),
        "time": time2, 
        "carbon_monoxide": carbon_monoxide,
        "pm2_5": pm2_5,
        "pm10": pm10
    })

    return InquinamentoByDate

def SettaPreferito(id:str):
    documento = coordinate_n.find_one({"id": id})
    
    if documento:
        preferito_attuale = documento.get("preferito", False)
        nuovo_valore_preferito = not preferito_attuale
        result = coordinate_n.update_one(
            {"id": id},
            {"$set": {"preferito": nuovo_valore_preferito}}
        )
        return result
    else:
        return None  

def RetrivePreferiti():
    trovati = coordinate_n.find({"preferito":True})
    listaCoordinate = []
    for trovato in trovati:
        id = str(trovato.get("id"))
        latitude = trovato.get("lat")
        longitude = trovato.get("lon")
        nazione = trovato.get("nazione")
        
        listaCoordinate.append({
            "id": id,
            "lat": latitude,
            "lon": longitude,
            "nazione": nazione
        })
    return listaCoordinate

def Filter_by_date_meteo(id: str, data: str) -> dict:
    # Costruzione della query
    query = {
        "_id": ObjectId(id),
        "measurements": {
            "$elemMatch": {
                "time": data,
                "precipitation": {"$gte": 0}
            }
        }
    }

    # Proiezione per includere solo le misurazioni che soddisfano il criterio di data
    projection = {
        "measurements": {
            "$filter": {
                "input": "$measurements",
                "as": "m",
                "cond": {
                    "$and": [
                        {"$eq": ["$$m.time", data]},
                        {"$gte": ["$$m.precipitation", 0]}
                    ]
                }
            }
        }
    }
    
    trovato = sensori.find_one(query, projection)
    if trovato is None:
        return None
    
    measurementsPrecipitation = []

    for m in trovato["measurements"]:
        # Determina se ha piovuto, nevicato o c'è stato il sole
        weather_condition = "sole"
        if m.get("precipitation", 0) > 0:
            if m.get("rain", False):
                weather_condition = "pioggia"
            elif m.get("snowfall", 0) > 0:
                weather_condition = "neve"
        
        measurementsPrecipitation.append({
            "relative_humidity_2m": m.get("relative_humidity_2m"),
            "precipitation": m.get("precipitation"),
            "rain": m.get("rain"),
            "snowfall": m.get("snowfall"),
            "weather_condition": weather_condition
        })
        
    Sensorebydate = {
        "id": id,
        "measurementsPrecipitation": measurementsPrecipitation,
    }
    return Sensorebydate