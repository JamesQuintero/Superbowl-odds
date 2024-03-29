import json
import os

from Utils import Utils


"""
Handles data scraped from Bovada.lv
"""
class BetMGM:
    utils = None

    def __init__(self, year):
        self.utils = Utils()

        self.heatmap_path = "./data/{}/heatmap_data.csv".format(year)
        self.betMGM_exact_score_odds_json_path = "./data/{}/BetMGM_exact_score_odds.json".format(year)
        self.betMGM_squares_odds_json_path = "./data/{}/BetMGM_squares_odds.json".format(year)

    def get_squares_odds(self):
        return self.get_odds(self.betMGM_squares_odds_json_path)

    def get_exact_score_odds(self):
        return self.get_odds(self.betMGM_exact_score_odds_json_path)

    """
    Returns 
        {
            "10,7": {
                "name": "Chiefs 10 - Eagles 7",
                "odds": 50000
            },
            "13,10": {
                "name": "Chiefs 13 - Eagles 10",
                "odds": 20000
            },
            ...
        }
    """
    def get_odds(self, path="./random_path"):
        if not os.path.exists(path):
            return {}

        contents = self.utils.read_json(path)['results']

        to_return = {}
        for row in contents:
            bet_name = row['name']['value']
            scores = self.extract_scores(bet_name)
            scores_str = self.utils.score_to_str(scores[0], scores[1])

            to_return[scores_str] = {
                "name": bet_name,
                "odds": row['americanOdds']
            }

        return to_return

    """
    Provided scores string "Chiefs 10 - Eagles 7", return [10, 7]
    """
    def extract_scores(self, scores_str):
        split_str = scores_str.split(" - ")
        first_score = int(split_str[0].split(" ")[-1])
        second_score = int(split_str[1].split(" ")[-1])
        return [first_score, second_score]


if __name__=="__main__":
    utils = Utils()
    year = utils.ask_year()
    analyzer = BetMGM(year)
    analyzer.get_odds()