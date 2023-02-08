import json
import os

from Utils import Utils


"""
Handles data scraped from Caesar's sportsbook.
"""
class Caesars:
    utils = None

    def __init__(self, year):
        self.utils = Utils()

        self.heatmap_path = "./data/{}/heatmap_data.csv".format(year)
        self.caesars_odds_json_path = "./data/{}/Caesars_odds.json".format(year)



    """
    Returns 
        {
            "4,7": {
                "name": "|Kansas City Chiefs| 4 |and| |Philadelphia Eagles| 7",
                "odds": 50000
            },
            "7,0": {
                "name": "|Kansas City Chiefs| 7 |and| |Philadelphia Eagles| 0",
                "odds": 20000
            },
            ...
        }
    """
    def get_odds(self):
        contents = self.utils.read_json(self.caesars_odds_json_path)
        squares = contents['markets'][0]['selections']

        to_return = {}
        for square in squares:
            bet_name = square['name']
            scores = self.extract_scores(bet_name)
            scores_str = self.utils.score_to_str(scores[0], scores[1])

            to_return[scores_str] = {
                "name": bet_name,
                "odds": square['price']['a']
            }

        return to_return

    """
    Provided scores string "|Kansas City Chiefs| 4 |and| |Philadelphia Eagles| 7", return [4, 7]
    """
    def extract_scores(self, scores_str):
        split_str = scores_str.split(" |and| ")
        first_score = int(split_str[0].split(" ")[-1])
        second_score = int(split_str[1].split(" ")[-1])
        return [first_score, second_score]


if __name__=="__main__":
    utils = Utils()
    year = utils.ask_year()
    analyzer = Caesars(year)
    analyzer.get_odds()