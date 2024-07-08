import hashlib
import datetime
import random
import json
from src.dbConnection import  utenti, sensori
from src import login_manager
from src.model import utente, sensore
from src.load_DB import main_load


from bson.objectid import ObjectId
from datetime import timedelta
from flask import request, render_template, session, jsonify, redirect, url_for
from src import app
from flask_login import current_user, login_required , login_user, logout_user


@app.route("/listaSensori",methods=["GET", "POST"])
@login_required
def listaSensori():
    nazione = request.args.get("nazione")
    if nazione:
        listaSensori = main_load.sensoriByNazione(nazione)
        return render_template("listaSensori.html", listaSensori=listaSensori)
    else :
        listaSensori = main_load.RetriveCoordinareSensori()
        return render_template("listaSensori.html", listaSensori=listaSensori)

@app.route("/sensoriPreferiti",methods=["GET", "POST"])
@login_required
def sensoriPreferiti():
    listaSensori = main_load.RetrivePreferiti()
    return render_template("sensoriPreferiti.html", listaSensori=listaSensori)

@app.route("/login",methods=["GET", "POST"])
def login():
        successo = False
        risposta ={
            "PasswordNonValida" : False,
        }
        
        if request.method != "POST":
            return render_template("login.html", risposta = risposta)
        if request.method == "POST":
            email = request.form.get("email")
            password = request.form.get("password")
            urlLastPage = request.form.get("next")
            redirectUrl = "listaSensori"
            tentativo_login: utente = main_load.UtentebyEmail(email)
            if not tentativo_login:
                        #Utente non Registato
                        successo = False
            if tentativo_login.password == password:
                        login_user(tentativo_login, duration= timedelta(days=365),force=True)
                        successo = True
            else:
                        #Passeord sbagiata 
                        successo = False
                        risposta["PasswordNonValida"] = True
            if successo:
                # Se ha provato ad accedere ad una pagina prima di arrivare al
                # login automaticamente:
                if (urlLastPage):
                    redirectUrl = urlLastPage
                return redirect(redirectUrl)
            else:
                return render_template("login.html", risposta = risposta)
        else:
            return render_template("login.html", risposta = risposta)

@login_manager.user_loader
def load_user(user_id):
        return main_load.UtentebyID(user_id)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("homepage"))

@app.route("/dettagliSensore", methods=["POST", "GET"])
def dettagliSensore():
    idsensore = request.args.get("idSensore")
    date_str = request.args.get("startDate")
    date_end_str = request.args.get("endDate")
    type_param = request.args.get("type")
    
    if type_param == "giornosingolo":
        date_str_n = date_str + "T03:00:00"
        date_str_i = date_str + "T03:00"
        sensore = main_load.Filter_by_date(idsensore, date_str_n)
        idSensoreMacro = sensore[0]['id']
        datiinquinamento = main_load.Filter_inquinamento_by_date(idSensoreMacro, date_str_i)
        datiPrecipitazioni = sensore[0]['measurementsPrecipitation']
        datiTemperatura = sensore[0]['measurementsTemperature']
        datiVento = sensore[0]['measurementsWind']
        return render_template("dettagliSensore.html", sensore=sensore, datiinquinamento=datiinquinamento,datiPrecipitazioni=datiPrecipitazioni, datiTemperatura=datiTemperatura, datiVento=datiVento)
    elif type_param == "giornosucc":
        date_str_n = date_str + "T03:00:00"
        date_str_i = date_str + "T03:00"
        sensore = main_load.Filter_by_date_gt(idsensore, date_str_n)
        idSensoreMacro = sensore[0]['id']
        datiinquinamento = main_load.Filter_inquinamento_by_date_gt(idSensoreMacro, date_str_i)
        datiPrecipitazioni = sensore[0]['measurementsPrecipitation']
        datiTemperatura = sensore[0]['measurementsTemperature']
        datiVento = sensore[0]['measurementsWind']
        return render_template("dettagliSensore.html", sensore=sensore, datiinquinamento=datiinquinamento,datiPrecipitazioni=datiPrecipitazioni, datiTemperatura=datiTemperatura, datiVento=datiVento)
    elif type_param == "rangegiorni":
        date_str_n = date_str + "T03:00:00"
        date_str_i = date_str + "T03:00"
        date_end_str_n = date_end_str + "T03:00:00"
        date_end_str_i = date_end_str + "T03:00"
        sensore = main_load.Filter_by_date_range(idsensore, date_str_n, date_end_str_n)
        idSensoreMacro = sensore[0]['id']
        datiinquinamento = main_load.Filter_inquinamento_by_date_range(idSensoreMacro, date_str_i, date_end_str_i)
        datiPrecipitazioni = sensore[0]['measurementsPrecipitation']
        datiTemperatura = sensore[0]['measurementsTemperature']
        datiVento = sensore[0]['measurementsWind']
        return render_template("dettagliSensore.html", sensore=sensore, datiinquinamento=datiinquinamento,datiPrecipitazioni=datiPrecipitazioni, datiTemperatura=datiTemperatura, datiVento=datiVento)
    else:
        sensore = main_load.SensorebyID(idsensore)
        idSensoreMacro = sensore[0]['id']
        datiinquinamento = main_load.RetriveInquinamentoBySensoredID(idSensoreMacro)
        datiPrecipitazioni = sensore[0]['measurementsPrecipitation']
        datiTemperatura = sensore[0]['measurementsTemperature']
        datiVento = sensore[0]['measurementsWind']
        return render_template("dettagliSensore.html", sensore=sensore, datiinquinamento=datiinquinamento,datiPrecipitazioni=datiPrecipitazioni, datiTemperatura=datiTemperatura, datiVento=datiVento)     

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error_pages/404.html'), 404


@app.route("/aggiungiSensore", methods=['GET', 'POST'])
@login_required
def aggiungiSensore():
    if(request.method != "POST"):
        return render_template("aggiungiSensore.html")
    elif request.method == "POST":
        richiesta = request.get_json()
        nome = richiesta.get("nomeSensore")
        posizioneSensore = richiesta.get("posizioneSensore")
        
        with open("coordinate.json", "r") as file:
            coordinate_data = json.load(file)
            
        random_entry = random.choice(coordinate_data)
        id = random_entry["id"]
        sensore = main_load.Retrive_one_Sensori(id)
        sensoreinqui = main_load.RetriveInquinamentoBySensoredID(id)
        "BISOGNA FARE L'INSERT DEI DATI INQUINAMENTO E DEI DATI METEO"
        control = True
        
        if control != None:
            return jsonify({"success": True, "Sensore": sensore,"datiinquimaneto": sensoreinqui})
        elif control == None:
            return jsonify({"success": False})
        
        
@app.route("/eliminaSensore", methods=['GET', 'POST'])
def eliminaSensore():
    if(request.method != "POST"):
        return redirect(url_for("listaSensori"))
    elif request.method == "POST":
        richiesta = request.get_json()
        idsensore = richiesta.get("idSensore")
        control = main_load.EliminaSensore(idsensore)
        if control != None:
            return jsonify({"success": True})
        elif control == None:
            return jsonify({"success": False})
        

        
@app.route("/register",methods=["GET", "POST"])
def register():
    if(request.method != "POST"):
        return render_template("register.html")
    if request.method == "POST":
        richiesta = request.form
        email = richiesta.get("email")
        nome = richiesta.get("nome")
        cognome = richiesta.get("cognome")
        password = richiesta.get("password")
        # Se l'email è già usata il server avviserà il front-end
        if main_load.UtentebyEmail(email) is not None:
            msg = "Email gia usata, si prega di inserirne un altra"
            return render_template("error_pages/custom_error.html", msg = msg)
        else:
            main_load.creaUtente(nome,cognome,email,password)
            return redirect(url_for("login"))
    return render_template("register.html")


@app.route('/contagiorni', methods=['GET', 'POST'])
@login_required  
def contagiorni():
    if request.method == 'POST':
        data = request.json
        idsensore = data['id']
        limite_inferiore = float(data['value'])
        dati_sensore = main_load.SensorebyID(idsensore)
        idMacroSensore = dati_sensore[0]['id']
        datiinquinamento = main_load.RetriveInquinamentoBySensoredID(idMacroSensore)
        if data['type'] == 'temperature':
            temperature = dati_sensore[0]['measurementsTemperature']
            result = [
                        {'valore_rilevazione': entry['temperature_2m'], 'time': entry['time']}
                        for entry in temperature
                        if entry['temperature_2m'] > limite_inferiore
            ]
            return jsonify({'success': True, 'data': result,'tipo': data['type']})
        elif data['type'] == 'wind':
            wind = dati_sensore[0]['measurementsWind']
            result = [
                        {'valore_rilevazione': entry['wind_speed_10m'], 'time': entry['time']}
                        for entry in wind
                        if entry['wind_speed_10m'] > limite_inferiore
            ]
            return jsonify({'success': True, 'data': result,'tipo': data['type']})
        elif data['type'] == 'precipitation':
            precipitation = dati_sensore[0]['measurementsPrecipitation']
            result = [
                        {'valore_rilevazione': entry['relative_humidity_2m'], 'time': entry['time']}
                        for entry in precipitation
                        if entry['relative_humidity_2m'] > limite_inferiore
            ]
            return jsonify({'success': True, 'data': result,'tipo': data['type']})
        elif data['type'] == 'inquinamento':
            result = []
            for entry in datiinquinamento:
                for i, pm2_5_value in enumerate(entry['pm2_5']):
                    if float(pm2_5_value) > limite_inferiore:
                        result.append({
                            'valore_rilevazione': float(pm2_5_value),
                            'time': entry['time'][i] if isinstance(entry['time'], list) else entry['time']
                        })
            return jsonify({'success': True, 'data': result, 'tipo': 'pm2.5'})


@app.route('/settapreferito', methods=['GET', 'POST'])
def settapreferito():
    if request.method == 'POST':
        data = request.json
        idsensore = data['id']
        control = main_load.SettaPreferito(idsensore)
        if control != None:
            return jsonify({"success": True})
        elif control == None:
            return jsonify({"success": False})



@app.route('/visitaeventi', methods=['GET', 'POST'])
@login_required  
def visitaeventi():
    if request.method == 'POST':
        data = request.json
        data_selezionate = data['date']
        idSensore = data['idSensore']
        data_finale = data_selezionate +"T03:00:00" 
        rilevazioni = main_load.Filter_by_date_meteo(idSensore, data_finale)
        if rilevazioni != None:
            return jsonify({"success": True, "data": rilevazioni})
        elif rilevazioni == None:
            return jsonify({"success": False})
