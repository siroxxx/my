from math import *
from requests import *
from segretoRouteService import TOKEN

def getDistanzaStrada(lat1, lat2, lon1, lon2):
    url=f"https://api.openrouteservice.org/v2/directions/driving-car?api_key={TOKEN}&start={lon1},{lat1}&end={lon2},{lat2}"
    resp=get(url)
    if resp.status_code==200:
        ret= resp.json()['features'][0]['properties']['segments'][0]['distance']
        return ret
    else:
        if resp.status_code==400:
            return "citta troppo distanti"
        else: return "err"

def getDistanzaInLineaDAria(lat1, lon1, lat2, lon2):
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
