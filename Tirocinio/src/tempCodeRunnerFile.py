
@app.route("/test", methods=["GET", "POST"])
def test():
    #user = current_user.id
    listaSensori = main_load.RetriveallSensori()
    #print("ecco la lista sensori ",listaSensori)
    return render_template("test.html", listaSensori = listaSensori)
