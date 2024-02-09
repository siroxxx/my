from requests import get
from datetime import datetime

class alphavantageApiManager:
    
    # Estrae i dati da alphavantage.co, dati simbolo del titolo azionario (ticker), mese (numerico), anno e l'API key.
    """
        L'obbiettivo di questo esercizio è creare un grafico che mostra l'andamento 
        dell'asset interessato nell'arco di un mese; più campioni ho nel corso di quel
        mese più preciso sarà il grafico. Il livello massimo offerto da alphavantage
        è un campione ogni 5 minuti, dunque, di base, specifico interval=5min.
    """
    def get_data(symbol, month, year, api_key):
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&month={year}-{month}&outputsize=full&apikey={api_key}"
        response = get(url)
        data = response.json()
        return data
    
    # Estrae i dati dal JSON ottenuti con get_data
    def extract_data(data):
        data = data["Time Series (5min)"] # Le informazioni che mi servono sono solo i campioni che nel JSON sono contenuti in "Time Series (5min)"
        # Trasformo data in un dizionario più leggibile
        """
            Per ogni campione estraggo data-orario (che è la chiave del campione) e valore, 
            trasformo i primi due in un oggetto datetime e aggiungo il nuov chiave-valore al dizionario.
            Attenzione: il valore è a sua volta un dizionario, che contiene valore di apertura,
            chiusura, massimo, minimo e volume del titolo azionario.
        """
        data = {datetime.strptime(key, "%Y-%m-%d %H:%M:%S"): value for key, value in data.items()} 
        
        """ 
            Se non l'avessi capito, per creare un nuovo oggetto datetime a partire da una stringa,
            è necessario che alla funzione strptime venga specificato il formato della data contenuta in essa,
            quindi la posizione di anno, mese, giorno, ora, minuto e secondo nella stringa passata.
        """
        
        return data