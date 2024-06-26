import flask_pymongo
from flask_pymongo import PyMongo
from src import app

#Connessione al provider mondoDbAltas
mongo = PyMongo(app)

#Assegnazione alla variabile db il database
db = mongo.db.client.MeteoAnalytisc

utenti = db.Utenti

sensori = db.Sensori
