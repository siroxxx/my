from requests import *
from time import sleep
def inviaLinkPosizione(latitudine, longitudine):
    return "https://www.openstreetmap.org/#map=18/" + latitudine + "/" + longitudine

def getCity(nome, index):
    url=f"https://nominatim.openstreetmap.org/search?q={nome}&format=json&addressdetails=1"
    resp=get(url)
    sleep(0.5)
    index=int(index)
    if resp.status_code==200:
        return resp.json()[index]["name"]
    else: return "err"
    
def getCodCountry(nome, index):
    url=f"https://nominatim.openstreetmap.org/search?q={nome}&format=json&addressdetails=1"
    resp=get(url)
    sleep(0.5)
    index=int(index)
    if resp.status_code==200:
        return resp.json()[index]["address"]["country_code"]
    else: return "err"
    
def getCitiesDesc(nome):
    url=f"https://nominatim.openstreetmap.org/search?q={nome}&format=json&addressdetails=1"
    resp=get(url)
    sleep(0.5)
    if resp.status_code==200:
        cities=[]
        for i in range(0, len(resp.json())):
            if(resp.json()[i]["addresstype"]!="county"):
                cities.append(resp.json()[i]["display_name"])
        return cities
    else: return "err"
    
def getLatByName(nome, index):
    url=f"https://nominatim.openstreetmap.org/search?q={nome}&format=json&addressdetails=1"
    resp=get(url)
    sleep(0.5)
    index=int(index)
    if resp.status_code==200:
        return resp.json()[index]["lat"]
    else: return "err"

def getLonByName(nome, index):
    url=f"https://nominatim.openstreetmap.org/search?q={nome}&format=json&addressdetails=1"
    resp=get(url)
    sleep(0.005)
    index=int(index)
    if resp.status_code==200:
        return resp.json()[index]["lon"]
    else: return "err"
