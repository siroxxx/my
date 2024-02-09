from requests import *

class TelegramBot:
    def __init__(self):
        self.token = "6400453810:AAEmXx9Yeqa9eTJ4yQVwVPki7KvGr1rqw4A"
        self.url = f"https://api.telegram.org/bot{self.token}/"

    def ricevi(self, lastid):
        urlRicevi = self.url + "getUpdates"
        parametri = {"offset": lastid}
        resp = get(urlRicevi, params=parametri)
        data = resp.json()
        return data

    def leggiMessaggio(self, data):
        try:
            lastMsg= data["result"][len(data["result"])-1]["message"]
            return data
        except:
            print("Errore")
            return None

    def checkNuovo(self, lastMsg, previousMsg):
        # Controllo se c'è un nuovo messaggio
        nuovoMex = False
        try:
            if lastMsg is not None and previousMsg != "":
                if lastMsg["message_id"] != previousMsg["message_id"]:
                    nuovoMex = True
                    print ("Utente: " + lastMsg["text"] + "\n")
        except:nuovoMex=False
        return nuovoMex

    def aggiornaLastId(self, lastid, data):
        # Aggiorna lastid
        if len(data["result"]) > 0:
            lastid += 1
        return lastid

    def invia(self, risposta, lastMsg):
        # Invia un messaggio
        chat_id = lastMsg["chat"]["id"]
        urlInvio = self.url + "sendMessage"
        if risposta == "":
            risposta = "Comando non riconosciuto"
        paramInvio = {"chat_id": chat_id, "text": risposta}
        resp2 = post(urlInvio, params=paramInvio)
        if resp2.status_code==True:
            if resp2["code"]==True:
                print (resp2["result"]) #se è giusto ritorna 200 OK