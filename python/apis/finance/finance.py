from segretoFinance import TOKEN
from requests import *
def getBilancioDaA(asset, start_date, end_date):
    # Simbolo dell'asset finanziario che desideri monitorare (es. 'AAPL' per Apple)
    symbol = asset

    # URL per ottenere dati storici giornalieri
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={TOKEN}'
    print(url)
    try:
        # Effettua la richie"sta API
        resp = get(url)
        #f = open("data.txt", "r")
        #data=f.read()
        #f.close()
        data = resp.json()

        # Estrai i dati relativi al periodo specificato
        daily_data = data['Time Series (Daily)']
        date=[]
        apertura=[]
        chiusura=[]
        massimo=[]
        minimo=[]
        assert data is not None, "ERRORE"
        for giorno in daily_data:
            if start_date <= giorno and giorno <= end_date:
                date.append(giorno)
                apertura.append(float(daily_data[giorno]["1. open"]))
                massimo.append(float(daily_data[giorno]["2. high"]))
                minimo.append(float(daily_data[giorno]["3. low"]))
                chiusura.append(float(daily_data[giorno]["4. close"]))
        return date, apertura, chiusura, massimo, minimo
    except Exception as e:
        print (f'Errore: {e}')
        return None, None
        