import json
import os

from Utils import Utils


"""
Handles data scraped from Bovada.lv
"""
class Bovada:
    utils = None

    def __init__(self, year):
        self.utils = Utils()

        self.bovada_odds_txt_path = "./data/{}/Bovada_odds.txt".format(year)
        self.bovada_odds_json_path = "./data/{}/Bovada_odds.json".format(year)
        self.heatmap_path = "./data/{}/heatmap_data.csv".format(year)



    """
    Assumes Bovada odds data in Bovada_odds.txt is in format
        Rams 0 Bengals 0 +3500
        Rams 1 Bengals 0 +6600
        Rams 2 Bengals 0 +10000
    """
    def transform_bovada_odds(self):

        if os.path.isfile(self.bovada_odds_json_path):
            print("Bovada odds already exist in {}".format(self.bovada_odds_json_path))
            return

        odds_txt = self.utils.read_from_txt(self.bovada_odds_txt_path)

        favored_team = -1
        
        to_save = {}
        to_save['teams'] = []
        to_save['odds'] = {}
        for row in odds_txt:
            split_row = row.split(" ")

            if favored_team == -1:
                favored_team = self.ask_team_odds(split_row[0], split_row[2])

            if favored_team == 0:
                score = self.utils.score_to_str(split_row[3], split_row[1])
                to_save['teams'] = [split_row[2], split_row[0]]
            else:
                score = self.utils.score_to_str(split_row[1], split_row[3])
                to_save['teams'] = [split_row[0], split_row[2]]

            to_save['odds'][score] = int(split_row[4].replace("+", ""))

        self.utils.save_to_json(self.bovada_odds_json_path, to_save)

    """
    Determines who is the favored team to know how to sort the bovada odds when converting from txt to json.
    """
    def ask_team_odds(self, team1, team2):
        choice = -1
        while choice != 1 and choice != 2:
            print("Teams playing: ")
            print("1) {}".format(team1))
            print("2) {}".format(team2))
            choice = int(input("Who has better odds of winning? (Team with minus/negative odds): "))

        return choice - 1

        # print("Look at Win odds for each team. (ex: -190 for favorable team)")
        # input("Odds for {} to win: ".format(team1))
        # input("Odds for {} to win: ".format(team2))
        # return 


if __name__=="__main__":
    utils = Utils()
    year = utils.ask_year()
    analyzer = Bovada(year)
    analyzer.transform_bovada_odds()