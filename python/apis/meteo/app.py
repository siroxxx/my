from openStreetMap import *
from openRouteService import *
from openWeatherMap import *
import os
def main():
    print("questo programma accetta in input una serie di città separate da virgola e spazio (es. Milano, Verona, ecc...) e ritorna:\n- km di strada tra una tappa e l'altra ( con il tempo stimato di viaggio )\n- condizioni meteo generali della giornata in quella città ( meteo, temp min e max ) \n- km totali del viaggio")
    while True:
        print("inserisci quante città prevede il tuo tour: \n")
        numcitta=int(input())
        errore=False
        distanzaTotale=0
        citta=[]#le città del tour
        indici=[]
        nazioni=[]
        for i in range(numcitta):
            print("inserisci la città "+str(i+1))
            cittaCorrente=input()
            print("Quale tra queste città è quella che vuoi selezionare? (inserisci il numero)")
            trovate=getCitiesDesc(cittaCorrente)
            for x in range(len(trovate)):
                print("-"+str(x)+":"+trovate[x])
            selezionata=input()
            os.system("cls")
            indici.append(selezionata)
            citta.append(getCity(cittaCorrente, selezionata))
            nazioni.append(getCodCountry(cittaCorrente, selezionata))
            
        print("città selezionate: ")
        for i in citta:
            print(i)
        print('\n')
        for i in range(len(citta)):
            if i!=len(citta)-1:
                try:
                    lat1=getLatByName(citta[i], indici[i])
                    lat2=getLatByName(citta[i+1], indici[i])
                    lon1=getLonByName(citta[i], indici[i])
                    lon2=getLonByName(citta[i+1], indici[i])
                except: 
                    print("città "+citta[i]+" errata")
                    errore=True
                
                distanza=int(getDistanzaStrada(lat1, lat2, lon1, lon2) )
                distanza=round(distanza/1000,3)
                distanzaTotale+=distanza 
                print("distanza tra "+citta[i]+" e "+citta[i+1]+" : "+str(distanza)+ " km")
            meteo=getMeteoByCitta(citta[i], nazioni[i])
            tempMin=round(toCelsius(meteo["main"]["temp_min"]), 3)
            tempMax=round(toCelsius(meteo["main"]["temp_max"]), 3)
            descMeteo=meteo["weather"][0]["description"]
            print("meteo a "+citta[i]+" : "+ descMeteo +"\n Temperatura min: "+str(tempMin)+"°C\n Temperatura max: "+str(tempMax)+"°C")
            
            
        print("distanza totale da percorrere: "+ str(round(distanzaTotale,3))+" km")
        print("\n")
            
if __name__ == "__main__":
    main()