from balldontlie import nba
from the_odds_api import *
import os
def main():
    n=nba()
    f=fresca()
    while True:
        print("Ciao, cosa vuoi fare?")
        print("-1 risultati partite NBA")
        print("-2 voglio giocare in NBA")
        print("-3 voglio ballare un po di fresca NBA")
        whatToDo=input()
        if whatToDo=="1":
            print("inserisci la stagione che ti interessa (corrente: 2023)")
            season=input()
            print("Seleziona un'opzione:")
            print("-1 partite di un giorno")
            print("-2 partite di una squadra in un certo periodo")
            print("-3 partita singola")
            whatToChoose=input()
            match whatToChoose:
                case "1":
                    print("inserisci la data YYYY-MM-DD")
                    date=input()
                    status, homeTeam, homeScore, guestScore, guestTeam=n.getDailyGames(season, date)
                case "2":
                    print("inserisci la squadra nel formato che preferisci (es. atl, atlanta, hawks, atlanta hawks)")
                    team=input()
                    print("inserisci la data iniziale YYYY-MM-DD")
                    datein=input()
                    print("inserisci la data finale YYYY-MM-DD")
                    datefin=input()
                    status, homeTeam, homeScore, guestScore, guestTeam=n.getTeamGames(season, team, datein, datefin)
                case "3":
                    print("inserisci la data YYYY-MM-DD")
                    date=input()
                    print("inserisci la squadra")
                    team=input()
                    status, homeTeam, homeScore, guestScore, guestTeam=n.getSingleGame(season, team, date)
                case _:
                    print("errore")
            assert homeTeam is not None, "PARTITE NON ESISTENTI PER IL GIORNO SELEZIONATO!!!" #basta controllare un qualsiasi vettore
            print()
            if whatToChoose!="3":
                for i in range(len(homeTeam)):
                    print (f"{i}: {status[i]} | {homeTeam[i]} {homeScore[i]}  - {guestScore[i]} {guestTeam[i]}")
            else:
                print (f"{status} | {homeTeam} {homeScore}  - {guestScore} {guestTeam}")          
            print()        
        elif whatToDo=="2": #https://free-apis.github.io/#/browse
            print("cazzo ci fai ancora qua, vai ad allenarti")
        elif whatToDo=="3": #https://free-apis.github.io/#/browse
            print("Mi raccomando, non ballare troppo, in che continente sei? (us, uk, au, eu)")
            regione=input()
            print("Che tipo di scommessa vuoi fare?")
            print("-h2h | vincitore")
            print("-spreads | punti di scarto tra le squadre")
            print("-totals | somma dei punteggi delle squadre sopra o sotto una certa soglia")
            tipo=input()
            resp=f.getDailyBets(regione, tipo)
            for x in resp:
                match tipo:
                    case "h2h" | "totals":
                        print(f"Partita: {x['home_team']} vs {x['away_team']}")
                    case "spreads":
                        print(f"Partita: {x['home_team']} {x['bookmakers'][0]['markets'][0]['outcomes'][0]['point']} vs {x['away_team']} {x['bookmakers'][0]['markets'][0]['outcomes'][1]['point']} | inizio: {x['commence_time']}")
                
                #xId=x["id"]
                # partite.append({
                #     "id": x["id"],
                #     "homeTeam": x["home_team"]
                #     "guestTeam": x["guest_team"]
                # })
                for y in x["bookmakers"]:
                    match tipo:
                        case "h2h" | "spreads":
                            print(f"\t{y['key']}: home {y['markets'][0]['outcomes'][0]['price']}, guest: {y['markets'][0]['outcomes'][1]['price']}")
                        case "totals":
                            print(f"\t{y['key']}: total = {y['markets'][0]['outcomes'][0]['point']} | OVER {y['markets'][0]['outcomes'][0]['price']}, UNDER: {y['markets'][0]['outcomes'][1]['price']}")
                print()            
                    # betsPartita.append({
                    #     "id": xId,
                    #     "azienda": y["key"],
                    #     "homeOdd": y["markets"][0]["outcomes"][0],
                    #     "guestOdd": y["markets"][0]["outcomes"][1]
                    # })
        else:
            print("errore")
    
    
    
if __name__=="__main__":
    main()