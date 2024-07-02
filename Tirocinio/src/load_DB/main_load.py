import hashlib , re, datetime
from src.dbConnection import  utenti,sensori,coordinate, inquinamento, coordinate_n
"from src import login_manager"
from src.model.utente import utente
from src.model.sensore import sensore
from bson.objectid import ObjectId
from flask import request, render_template, session, jsonify, redirect
from src import app
from flask_login import current_user, login_required

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

        listaCoordinate.append({
            "id": id,
            "lat": latitude,
            "lon": longitude
        })
    return listaCoordinate

# Query per il recupero dei dati di un sensore in una data sepcifca
def Filter_by_date (id: str, data: str) -> sensore:
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
        "measurements": {
            "$filter": {
                "input": "$measurements",
                "as": "m",
                "cond": {"$eq": ["$$m.time", data]}
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
        "measurementsPrecipitation": measurementsPrecipitation,
        "measurementsWind": measurementsWind,
        "measurementsTemperature": measurementsTemperature
    })

    return Sensorebydate


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
        "measurementsPrecipitation": measurementsPrecipitation,
        "measurementsWind": measurementsWind,
        "measurementsTemperature": measurementsTemperature
    })

    return Sensorebydategt

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
        "measurementsPrecipitation": measurementsPrecipitation,
        "measurementsWind": measurementsWind,
        "measurementsTemperature": measurementsTemperature
    })

    return Sensorebydate