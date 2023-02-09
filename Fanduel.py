import os

from Utils import Utils

"""
Handles data scraped from Fanduel's sportsbook.
"""
class Fanduel:
    utils = None

    def __init__(self, year):
        self.utils = Utils()

        self.heatmap_path = "./data/{}/heatmap_data.csv".format(year)
        self.fanduel_squares_odds_json_path = "./data/{}/Fanduel_squares_odds.json".format(year)
        self.fanduel_exact_scores_odds_json_path = "./data/{}/Fanduel_exact_score_odds.json".format(year)


    def get_squares_odds(self):
        return self.get_odds(self.fanduel_squares_odds_json_path)

    def get_exact_score_odds(self):
        return self.get_odds(self.fanduel_exact_scores_odds_json_path)

    """
    Returns 
        {
            "4,7": {
                "name": "Eagles 0 - Chiefs 0",
                "odds": 50000
            },
            "7,0": {
                "name": "Eagles 0 - Chiefs 1",
                "odds": 20000
            },
            ...
        }
    """
    def get_odds(self, path="./random_path"):
        if not os.path.exists(path):
            return {}

        contents = self.utils.read_json(path)
        items = contents['runners']

        to_return = {}
        for item in items:
            bet_name = item['runnerName']
            scores = self.extract_scores(bet_name)
            scores_str = self.utils.score_to_str(scores[0], scores[1])

            to_return[scores_str] = {
                "name": bet_name,
                "odds": item['winRunnerOdds']['americanDisplayOdds']['americanOddsInt']
            }

        return to_return

    """
    Provided scores string "Eagles 12 - Chiefs 47", return [12, 47]
    """
    def extract_scores(self, scores_str):
        split_str = scores_str.split(" - ")
        first_score = int(split_str[0].split(" ")[-1])
        second_score = int(split_str[1].split(" ")[-1])
        return [first_score, second_score]


if __name__=="__main__":
    utils = Utils()
    year = utils.ask_year()
    analyzer = Fanduel(year)
    # analyzer.get_squares_odds()
    analyzer.get_exact_score_odds()