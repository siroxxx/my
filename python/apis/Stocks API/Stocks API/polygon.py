from requests import get
from datetime import datetime

class polygonApiManager:  

    # Funzione per estrarre i dati da polygon.io
    """
        Anche qui intervallo di 5 minuti (range/5/minute).
        C'è un' unica differenza rilevante con alphavantage:polygon frammenta il JSON in più part se ci sono troppi dati,
        ed è proprio quello che succede nel mio caso visto che prelevo un dato ogni 5 minuti per 31 giorni.
        Per questo motivo il JSON contiene un valore "next_url" che reindirizza alla prossima parte del JSON.
        Dunque, finchè questo valore è presente, devo continuare a fare richieste al server.
    """
    def get_data(symbol, month, year, api_key):
        url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/5/minute/{year}-{month}-01/{year}-{month}-31?apiKey={api_key}"
        response = get(url)
        data = response.json()
        
        if "next_url" in data:
            next_url = data["next_url"]
            while next_url:
                response = get(next_url + f"&apiKey={api_key}") # next_url in sè non contiene l'API key
                data_next = response.json()
                data["results"] += data_next["results"]
                next_url = data_next["next_url"] if "next_url" in data_next else None # if in one line
                
        return data

    # Funzione per estrarre i dati da polygon.io
    def extract_data(data):
        data = data["results"] # Le informazioni che mi servono sono solo i campioni che nel JSON sono contenuti in "results"
        """
            Come alphavantage, ma usa come chiave il timestamp in millisecondi,
            dove per ogni campione d corrisponde d["t"].
            Inoltre, ai normali valori di apertura, chiusura, massimo, minimo e volume,
            polygon aggiunge anche volume ponderato ["vw"] e numero di transazioni ["n"].
        """
        data = {datetime.fromtimestamp(d["t"]/1000): d for d in data}
        return data

