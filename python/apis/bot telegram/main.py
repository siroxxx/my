from json import *
from requests import *
from time import sleep
from pandas import *
from pymysql import *
from io import StringIO
from math import *

from telegram import TelegramBot
from db import DatabaseHandler

def calculate_distance(lat1, lon1, lat2, lon2):
    # Raggio della Terra
    R = 6371.0

    # Conversione in radianti
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    # Differenza di longitudine e latitudine
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    # Formula di Haversine
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

def main():

    bot = TelegramBot() 
    db=DatabaseHandler('localhost', 'root', '', 'db_benzina' )


    lastid=0;
    previousMsg=""
    stato="" #in che stato è il bot: può essere in nuovo, ricerca, niente ("")

    #lettura file memoria per le configurazioni precedenti
    nomeMacchina=""
    tipoCarburante=""
    capSerbatoio=""
    kmMassimi=""

    #lettura e scrittura 
    # file=open("configuration.txt")
    # content=file.read()

    # if(content !="" and content != None):
    #     content = ast.literal_eval(content) #trasforma in lista
    #     tipoCarburante=content[0]
    #     capSerbatoio=content[1]
    #     kmMassimi=content[2]
    #     nomeMacchina=content[3]
    # file.close()
    #parametri: &start=84893.434749&end=39375.5438743897
    latitudine=""
    longitudine=""
    contaRicerca=0 #quanod si ricerca prima si invia prima la psizione poi le altre cose
    while True:
        
        risposta="" #cio che deve rispondere il bot        
        data=bot.ricevi(lastid)
        lastMsg=bot.leggiMessaggio(data)
        try: #ricevi una posizione
            if contaRicerca!=1:
                msgTxt=lastMsg["text"]; #testo del messaggio
            else: #ricevi un messaggio normale
                latitudine= data["result"][len(data["result"])-1]["message"]["location"]["latitude"]
                longitudine = data["result"][len(data["result"])-1]["message"]["location"]["longitude"]
                contaRicerca=2
        except: 
            print("errore")
        #lastid = data["result"][len(data["result"])-1]["update_id"] #[len(data["result"])-1]
        nuovoMex=bot.checkNuovo(lastMsg, previousMsg)
        previousMsg = lastMsg
        lastid=bot.aggiornaLastId(lastid, data)

        #switch case comandi
        if nuovoMex==True:
            if stato=="":
                campi=msgTxt.split(" ")
                match campi[0]: #perchè nel select il comando ha sia la parola che il nome della macchina da selezionare
                    case "Select":
                        if len(campi)>1:
                            nome=campi[1]
                            query = "SELECT * FROM utenti where nome='"+nome+"'"
                            result=db.read_query(query)
                            if len(result) >0:
                                nomeMacchina=str(result["nome"][0])
                                tipoCarburante=str(result["tipocarburante"][0])
                                capSerbatoio=str(result["capacita"][0])
                                kmMassimi=str(result["maxkm"][0] )
                                risposta="macchina selezionata"
                            else : risposta="macchina non trovata"
                    case "New":
                        stato="nuovo"
                        risposta="inserisci i seguenti campi separati da uno spazio con la prima lettera maiuscola: \n -tipo di carburante \n -capacità del serbatoio \n -chilometri massimi con un pieno \n -nome della vettura"
                    case "Search":
                        if nomeMacchina=="":
                            risposta="seleziona prima una macchina utilizzando il comando: select NOME_MACCHINA"
                        else:
                            stato="ricerca"
                            contaRicerca=1
                            risposta="condividi la tua posizione"
            elif stato=="nuovo":               
                    try:
                        stato=""
                        campi=msgTxt.split(" ")
                        tipoCarburante=campi[0]
                        capSerbatoio=campi[1]
                        kmMassimi=campi[2]
                        nomeMacchina=campi[3]
                        query = "INSERT INTO utenti (nome, tipocarburante, capacita, maxkm) VALUES ('"+nomeMacchina+"', '"+tipoCarburante+"', '"+capSerbatoio+"', '"+kmMassimi+"')"
                        db.insert_query(query)
                        risposta="macchina creata e selezionata"

                    #per farlo su file
                    # file=open("configuration.txt", "w")
                    # dump(campi, file)
                    # file.close()
                    # risposta="creazione completata"
                    except:
                        risposta="errore nella scrittura dei parametri"
                        stato="nuovo" #rimetto lo stato a nuovo

            elif stato=="ricerca":
                if contaRicerca==3:
                    campi=msgTxt.split(" ")
                    if len(campi)==2 :
                        vicinOConven=campi[0]    
                        benzRimasta=campi[1]
                        stato=""
                        contaRicerca=0
                        latSelezionata=0
                        lonSelezionata=0
                        query = "SELECT latitudine, longitudine, descCarburante, prezzo FROM benzinai JOIN impianti on benzinai.idImpianto=impianti.idImpianto"
                        result=db.read_query()
                        latSelezionata=0
                        lonSelezionata=0
                        mindist=10000000 #variabili che uso per salvarmi i dati
                        minprezzo=1000000.0 #usata solo per la diistanza 
                        for i in range(len(result)):
                            if result["descCarburante"][i]==tipoCarburante:
                                calcolo=calculate_distance(latitudine, longitudine,result["latitudine"][i], result["longitudine"][i])
                                if vicinOConven==1: #vicinanza
                                    if calcolo < mindist and calcolo < benzRimasta:
                                        mindist = calcolo
                                        minprezzo=result["prezzo"][i]
                                        latSelezionata=result["latitudine"][i]
                                        lonSelezionata=result["longitudine"][i]
                                else: #convenienza
                                    if calcolo < float(benzRimasta) and result["prezzo"][i]<minprezzo:
                                        mindist=calcolo #salvo la distanza
                                        minprezzo=result["prezzo"][i] #salvo il min prezzo
                                        latSelezionata=result["latitudine"][i]
                                        lonSelezionata=result["longitudine"][i]
                                if latSelezionata !=0:
                                    mindist=round(mindist, 2)
                                    risposta= f"Benzinaio caldo a {mindist} km da te con {tipoCarburante} a {minprezzo}:\n"
                                    risposta+="https://www.openstreetmap.org/#map=18/" + str(latSelezionata) + "/" + str(lonSelezionata)
                                else: risposta="benzinaio non trovato"
                    else: risposta="campi non inseriti in maniera corretta"            
                elif contaRicerca==2:
                    contaRicerca=3
                    risposta="inserisci i seguenti campi separati da uno spazio: \n -vicinanza o convenienza (scrivere 1 per impostare vicinanza come preferenza viceversa scrivere 2) \n -km rimasti prima di andare a secco "


            #risposta del bot
            bot.invia(risposta, lastMsg)
            risposta=""
            
        #frequenza di controllo nuovi messaggi
        sleep(5)

if __name__ == "__main__":
    main()