from urllib.request import Request, urlopen

import requests
from bs4 import BeautifulSoup
import ast

class Webscraping:
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    def show_results(self, player_name):
        atp_url = "https://www.atptour.com/en/-/ajax/PredictiveContentSearch/GetPlayerResults/"

        player_name = player_name.strip()
        player_name_spaces = player_name.replace(" ", "%20")

        atp_url = atp_url + player_name_spaces

        try:
            atp_response = requests.get(atp_url, headers=self.headers)
            atp_data = atp_response.json()
            atp_data = atp_data["items"]
        except:
            return None

        players_list = []
        for player in atp_data:
            player_data = {
                "full_name": f"{player['FirstName']} {player['LastName']}",
                "atp_url": player["Url"],
                "id": player["Url"][player["Url"].rfind('/')-4:player["Url"].rfind('/')]
                }
            
            if player["ImageUrl"] != "":
                player_data["image_url"] = "https://atptour.com/" + player["ImageUrl"]

            players_list.append(player_data)
        
        return players_list

    def webscrape(self, player_info):
        player_info = ast.literal_eval(player_info)

        """player_info = {
        "full_name": "",
        "current_ranking": "",
        "country": "",
        "prize_money": "",
        "num_titles": "",
        "win_loss_record": "",
        "career_high": "",
        "total_slams": 0
        }"""

        player_url = "https://www.atptour.com" + player_info["atp_url"]
        
        req = Request(url=player_url, headers=self.headers)

        try:
            source = urlopen(req).read()
        except:
            return None

        soup = BeautifulSoup(source, "html5lib")
        
        ranking = soup.find(class_="data-number")
        player_info["current_ranking"] = ranking.text if ranking.text.strip() else "Unranked"
        
        country = soup.find(class_ = "player-flag-code")
        player_info["country"] = country.text if country and country.text.strip() else "Unknown"

        table = soup.find("table", id="playersStatsTable")
        rows = table.find_all("tr")
        columns = rows[1].find_all("td")
        
        player_info["prize_money"] = columns[4].find("div", "stat-value").text.strip() if columns[4].find("div", "stat-value").text.strip() else 0
        player_info["num_titles"] = columns[3].find("div", "stat-value").text.strip() if columns else 0
        player_info["win_loss_record"] = columns[2].find("div", "stat-value").text.strip() if columns else "0-0"
        player_info["career_high"] = columns[1].find("div", "stat-value").text.strip() if columns else 0

        lot_url = "https://www.landoftennis.com/statistics_men/grand_slam_most_titles.htm"
        req = Request(url=lot_url, headers=self.headers)
        source = urlopen(req).read()
        soup = BeautifulSoup(source, "html5lib") 
        
        table = soup.find_all("tr", class_=["a-top bt", "a-top"])

        player_info["total_slams"] = 0

        for row in table:
            name = row.find("td", class_="a-left")
            if str(name.text).lower() == f"{str(player_info['full_name']).lower()}":
                total_slams = row.find("td", class_="negri")
                player_info["total_slams"] = int(total_slams.text)

        return player_info