from requests import *
class nba:
    baseURL="https://www.balldontlie.io/api/v1/games/"
    teamFN=["","Atlanta Hawks","Boston Celtics","Brooklyn Nets","Charlotte Hornets","Chicago Bulls","Cleveland Cavaliers","Dallas Mavericks","Denver Nuggets","Detroit Pistons","Golden State Warriors","Houston Rockets","Indiana Pacers","Los Angeles Clippers","Los Angeles Lakers","Memphis Grizzlies","Miami Heat","Milwaukee Bucks","Minnesota Timberwolves","New Orleans Pelicans","New York Knicks","Oklahoma City Thunder","Orlando Magic","Philadelphia 76ers","Phoenix Suns","Portland Trail Blazers","Sacramento Kings","San Antonio Spurs","Toronto Raptors","Utah Jazz","Washington Wizards"]
    
    def getTeamId(self,team):
        for i in range(len(self.teamFN)):
            if team.lower() in self.teamFN[i].lower():
                return self.teamFN[i], i
        return -1
    
    def getTeamGames(self, season, team, datein, datefin):
        homeTeam, id=self.getTeamId(team)
        assert id != -1, "ERORRE"
        params = {
            "seasons[]": season,
            "team_ids[]": id,
            "start_date": datein,
            "end_date": datefin
            }
        resp=get(self.baseURL, params=params)
        resp=resp.json()
        resp=resp["data"]
        status=[]
        homeTeam=[]
        homeScore=[]
        guestTeam=[]
        guestScore=[]
        for x in resp:
            status.append(x["status"])
            homeTeam.append(x["home_team"]["full_name"])
            homeScore.append(x["home_team_score"])
            guestTeam.append(x["visitor_team"]["full_name"])
            guestScore.append(x["visitor_team_score"])
        return status, homeTeam, homeScore, guestScore, guestTeam #l'ordine in cui andranno visualizzati (final Atlanta Hawks 123 - 121 Boston Celtics)
            
    
    def getSingleGame(self, season, team, date):
        team, id=self.getTeamId(team)
        assert id != -1, "ERORRE"
        params = {
            "seasons[]": season,
            "team_ids[]": id,
            "start_date": date,
            "end_date": date
            }
        resp=get(self.baseURL, params=params)
        resp=resp.json()
        status=resp["data"][0]["status"]
        homeTeam=resp["data"][0]["home_team"]["full_name"]
        homeScore=resp["data"][0]["home_team_score"]
        guestTeam=resp["data"][0]["visitor_team"]["full_name"]
        guestScore=resp["data"][0]["visitor_team_score"]
        return status, homeTeam, homeScore, guestScore, guestTeam #l'ordine in cui andranno visualizzati (final Atlanta Hawks 123 - 121 Boston Celtics)
    
    def getDailyGames(self, season, date):
        params = {
            "seasons[]": season,
            "start_date": date,
            "end_date": date
            }
        status=[]
        homeTeam=[]
        homeScore=[]
        guestTeam=[]
        guestScore=[]
        resp=get(self.baseURL, params=params)
        resp=resp.json()
        resp=resp["data"]
        for x in resp:
            status.append(x["status"])
            homeTeam.append(x["home_team"]["full_name"])
            homeScore.append(x["home_team_score"])
            guestTeam.append(x["visitor_team"]["full_name"])
            guestScore.append(x["visitor_team_score"])
        return status, homeTeam, homeScore, guestScore, guestTeam #l'ordine in cui andranno visualizzati (final Atlanta Hawks 123 - 121 Boston Celtics)
            
        