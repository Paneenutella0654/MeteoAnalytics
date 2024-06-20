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
      
def RetriveSensori(propietarioid:str):
    if propietarioid != None:
        trovati = sensori.find({"propietario": propietarioid})
        listaSensori = []
        for trovato in trovati:
            id2 = str(trovato.get("_id"))
            name = str(trovato.get("name"))
            box_type = str(trovato.get("box_type"))
            exposure = str(trovato.get("exposure"))
            model = str(trovato.get("model"))
            propietario = str(trovato.get("propietario"))
            loc = trovato.get("loc")
            sensor = trovato.get("sensors")
            new_Sensore = sensore(id2,name,box_type,exposure,model,propietario,loc,sensor)
            listaSensori.append(new_Sensore)
    else:
        listaSensori = []
    return listaSensori 

def SensorebyID (id : str) -> sensore:
    trovato = sensori.find_one({"_id": ObjectId(id)})
    if trovato is None:
        return None
    id = str(trovato.get("_id"))
    name = str(trovato.get("name"))
    box_type = str(trovato.get("box_type"))
    exposure = str(trovato.get("exposure"))
    model = str(trovato.get("model"))
    propietario = str(trovato.get("propietario"))
    loc = trovato.get("loc")
    sensor = trovato.get("sensors")
    new_Sensore = sensore(id,name,box_type,exposure,model,propietario,loc,sensor)
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
      
