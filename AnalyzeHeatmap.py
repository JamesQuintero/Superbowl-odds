import json
import os

from Utils import Utils

class AnalyzeHeatmap:

    bovada_odds_txt_path = "./data/2022/Bovada_odds.txt"
    bovada_odds_json_path = "./data/2022/Bovada_odds.json"
    heatmap_path = "./data/2022/heatmap_data.json"

    def __init__(self):
        self.utils = Utils()

    """
    Prints and returns list of scores that are profitable to bet on
    """
    def analyze(self):
        score_probabilities, squares_probabilities = self.get_heatmap_likelihoods()
        self.print_heatmap_likelihoods(score_probabilities, squares_probabilities)


        bovada_squares_odds = self.utils.read_json(self.bovada_odds_json_path)['odds']

        print("Squares odds:")
        to_return = {}
        for row in squares_probabilities:
            score = row['score']
            bookie_percentage_likelihood = self.utils.get_percentage_likelihood_from_odds(bovada_squares_odds[score])
            calculated_likelihood = row['probability']
            calculated_min_odds = self.utils.get_odds_from_percentage_likelihood(row['probability'])

            if bookie_percentage_likelihood < calculated_likelihood:
                print("{}) Odds given: {}, Projected odds: {}".format(score, bovada_squares_odds[score], calculated_min_odds))
                to_return[score] = {"given_odds": bovada_squares_odds[score], "calculated_odds": calculated_min_odds, "given_probability": bookie_percentage_likelihood, "calculated_probability": calculated_likelihood}

        return to_return



    """
    Reads scores from heatmap_data.json, and determines which are most likely. 
    Returns two lists
        one for list of most likely actual score combinations.
        one for list of most likely squares score combinations. 
    """
    def get_heatmap_likelihoods(self):
        data = self.read_json(self.heatmap_path)

        overall_score_heatmap = {}
        squares_heatmap = {}

        total_games = 0
        for row in data['matrix']:
            for item in row:
                if item['count'] > 0:
                    score_str = self.utils.score_to_str(item['pts_lose'], item['pts_win'])
                    overall_score_heatmap[score_str] = item['count']


                    squares_score_str = self.utils.score_to_str(item['pts_lose']%10, item['pts_win']%10)
                    if squares_score_str not in squares_heatmap:
                        squares_heatmap[squares_score_str] = 0
                    squares_heatmap[squares_score_str] += item['count']

                    total_games += item['count']


        sorted_heatmap = dict(sorted(overall_score_heatmap.items(), key=lambda item: item[1], reverse=True))
        sorted_square_heatmap = dict(sorted(squares_heatmap.items(), key=lambda item: item[1], reverse=True))


        to_return_heatmap = []
        for score in sorted_heatmap:
            to_return_heatmap.append({"score": score, "count": sorted_heatmap[score], "probability": sorted_heatmap[score]/total_games})

        to_return_squares_heatmap = []
        for score in sorted_square_heatmap:
            to_return_squares_heatmap.append({"score": score, "count": sorted_square_heatmap[score], "probability": sorted_square_heatmap[score]/total_games})

        return to_return_heatmap, to_return_squares_heatmap

    """
    Prints out results of calculated sorted list of score likelihoods
    """
    def print_heatmap_likelihoods(self, sorted_heatmap, sorted_square_heatmap):
        def print_score_probabilities(heatmap_probabilities):
            for row in heatmap_probabilities:
                print("{}) {}, {}%".format(row['score'], row['count'], row['probability']*100))

        print("Score heatmap sorted by count:")
        print_score_probabilities(sorted_heatmap)
        print()
        print("Square game heatmap sorted by count:")
        print_score_probabilities(sorted_square_heatmap)
        print()
        # print("Total games: {}".format(total_games))
        # print()


if __name__=="__main__":
    analyzer = AnalyzeHeatmap()
    analyzer.analyze()