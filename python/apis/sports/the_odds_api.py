from segretoodds import TOKEN
from requests import *
class fresca: #https://the-odds-api.com/liveapi/guides/v4/#parameters-2
    baseUrl=f"https://api.the-odds-api.com/v4/sports/basketball_nba/odds/?apiKey={TOKEN}"
    #params -regioni -tipo di bet -inizio(2023-09-10T23:59:59Z) -fine
    def getDailyBets(self, regione, tipoBet):
        # inizio=f"{Giorno}T00:00:00Z"
        # fine=f"{Giorno}T23:59:59Z"
        params={
            "regions":regione,
            "markets":tipoBet
            #"commenceTimeFrom":inizio,
            #"commenceTimeTo":fine
        }
        resp=get(self.baseUrl, params=params)
        resp=resp.json()
        return resp
        #print(resp)