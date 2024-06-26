import hashlib , re
from src.dbConnection import  utenti,sensori
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
      
def RetriveallSensori():
    print("sono dentro la funzione RetriveallSensori")
    trovati = sensori.find()
    listaSensori = []
    print("sto Fuori dal for")
    for trovato in trovati:
        id2 = str(trovato.get("_id"))
        print("sto dentro il for")
        latitude = trovato.get("latitude")
        longitude = trovato.get("longitude")
        measurements = [
            {
                "time": m["time"],
                "temperature_2m": m.get("temperature_2m"),
                "relative_humidity_2m": m.get("relative_humidity_2m"),
                "precipitation": m.get("precipitation"),
                "rain": m["rain"],
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
        
        new_Sensore = sensore(id2, latitude, longitude, measurements)
        listaSensori.append(new_Sensore)
    
    return listaSensori

def SensorebyID (id : str) -> sensore:
    trovato = sensori.find_one({"_id": ObjectId(id)})
    if trovato is None:
        return None
    id2 = str(trovato.get("_id"))
    latitude = trovato.get("latitude")
    longitude = trovato.get("longitude")
    measurements = [
        {
            "time": m["time"],
            "temperature_2m": m.get("temperature_2m"),
            "relative_humidity_2m": m.get("relative_humidity_2m"),
            "precipitation": m.get("precipitation"),
            "rain": m["rain"],
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
    new_Sensore = sensore(id2, latitude, longitude, measurements)
    return new_Sensore

def AggiungiSensore(name: str, box_type: str, exposure: str, model: str, propietario: str, loc: dict, sensors: dict):
    result = sensori.insert_one({"name":name,"box_type":box_type,"exposure":exposure,"model":model,"propietario":propietario,"loc":loc,"sensors":sensors})
    return result
      
def EliminaSensore(id: str):
    result = sensori.delete_one({"_id": ObjectId(id)})
    return result
      
def ModificaSensore(id: str, name: str, box_type: str, exposure: str, model: str, propietario: str, loc: dict, sensors: dict):
    result = sensori.update_one({"_id": ObjectId(id)},{"$set":{"name":name,"box_type":box_type,"exposure":exposure,"model":model,"propietario":propietario,"loc":loc,"sensors":sensors}})
    return result

def creaUtente(nome: str, cognome: str, email: str, password: str):
          result = utenti.insert_one({"nome":nome,"cognome":cognome,"password":password,"email":email})
          return result
      
