from datetime import datetime
import hashlib
import json

# Scheletro della classe utente così come è presente sul database


class utente():
    def __init__(self, id: str, email: str, password: str, nome: str, cognome: str, ruolo: str):
        self.id = id
        self.nome = nome
        self.cognome = cognome
        self.email = email
        self.password = password
        self.ruolo = ruolo

    def get_id(self):
        try:
            return str(self.id)
        except AttributeError:
            raise NotImplementedError("No `id` attribute - override `get_id`")

    # Se esiste, allora è autenticato, perciò true. Serve per @login_required.
    def is_authenticated(self):
        return True

    def is_active(self):  # Controlla che l'utente non sia stato cancellato (Potrebbe essere utile per rimuovere ruoli, o cancellazione terreno.)
        return True

    # Se esiste, di sicuro non può essere anonimo, perciò false. Serve per
    # @login_required.
    def is_anonymous(self):
        return False

    def __eq__(self, __o: object) -> bool:
        if(self.nome == __o.nome and self.cognome == __o.cognome and self.email == __o.email and self.ruolo == __o.ruolo and self.password == __o.password):
           return True 
        else:
            return False
        

