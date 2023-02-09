import json
import os

from Utils import Utils


"""
Handles data scraped from DraftKing's sportsbook.
"""
class DraftKings:
    utils = None

    def __init__(self, year):
        self.utils = Utils()

        self.heatmap_path = "./data/{}/heatmap_data.csv".format(year)
        self.draftkings_exact_score_odds_json_path = "./data/{}/DraftKings_exact_score_odds.json".format(year)
        self.draftkings_squares_odds_json_path = "./data/{}/DraftKings_squares_odds.json".format(year)

    def get_squares_odds(self):
        return self.get_odds(self.draftkings_squares_odds_json_path)

    def get_exact_score_odds(self):
        return self.get_odds(self.draftkings_exact_score_odds_json_path)


    """
    Returns 
        {
            "27,30": {
                "name": "PHI Eagles 27:30 KC Chiefs",
                "odds": 8000
            },
            "27,31": {
                "name": "PHI Eagles 27:31 KC Chiefs",
                "odds": 9000
            },
            ...
        }
    """
    def get_odds(self, path="./random_path"):
        if not os.path.exists(path):
            print("Path doesn't exist: {}".format(path))
            return {}

        contents = self.utils.read_json(path)
        items = contents['offerSubcategory']['offers'][0][0]['outcomes']

        to_return = {}
        for item in items:
            bet_name = item['label']
            scores = self.extract_scores(bet_name)
            scores_str = self.utils.score_to_str(scores[0], scores[1])

            to_return[scores_str] = {
                "name": bet_name,
                "odds": int(item['oddsAmerican'].replace("+", ""))
            }

        return to_return

    """
    Provided scores string "PHI Eagles 27:30 KC Chiefs", return [27, 30]
    """
    def extract_scores(self, scores_str):
        split_str = scores_str.split(":")
        first_score = int(split_str[0].split(" ")[-1])
        second_score = int(split_str[1].split(" ")[0])
        return [first_score, second_score]


if __name__=="__main__":
    utils = Utils()
    year = utils.ask_year()
    analyzer = DraftKings(year)
    print(analyzer.get_exact_score_odds())