from requests import *
from segretoWeatherMap import TOKEN

def toCelsius(kelvin):
    celsius = kelvin - 273.15
    return celsius

def getMeteoByCitta(citta, codNazione):
    url=f"https://api.openweathermap.org/data/2.5/forecast?q={citta},{codNazione}&appid={TOKEN}"
    resp=get(url)
    if resp.status_code==200:
        return resp.json()['list'][0] 
    # tempMin=meteo["main"]["temp_min"]
    # tempMax=meteo["main"]["temp_max"]
    # descMeteo=meteo["weather"][0]["description"]
    else: return "err"
    
