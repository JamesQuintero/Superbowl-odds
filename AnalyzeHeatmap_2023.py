import json
import os

from Utils import Utils
from BetMGM import BetMGM
from Caesars import Caesars

class AnalyzeHeatmap_2023:
    heatmap_path = "./data/2023/heatmap_data.json"
    frequency_path = "./data/2023/frequency_data.csv"

    utils = None
    betMGM = None
    caesars = None

    def __init__(self):
        self.utils = Utils()
        self.year = self.utils.ask_year()
        self.betMGM = BetMGM(self.year)
        self.caesars = Caesars(self.year)


    """
    Prints and returns list of scores that are profitable to bet on
    """
    def analyze_exact_scores(self):
        score_probabilities, squares_probabilities = self.get_heatmap_likelihoods()
        self.print_heatmap_likelihoods(score_probabilities, squares_probabilities)

        betMGM_score_odds = self.betMGM.get_odds()
        # bet_MGM_score_odds = bookie_odds

        print("Score odds:")
        to_return = {}
        for row in score_probabilities:
            score = row['score']

            if score not in betMGM_score_odds:
                # print("Score {} isn't available for betting in betMGM".format(score))
                continue

            bookie_percentage_likelihood = self.utils.get_percentage_likelihood_from_odds(betMGM_score_odds[score]['odds'])
            # print("BetMGM odds: {}".format(bookie_percentage_likelihood))

            calculated_likelihood = row['probability']
            calculated_min_odds = self.utils.get_odds_from_percentage_likelihood(row['probability'])

            if bookie_percentage_likelihood < calculated_likelihood*1.0:
                print("{}) Should bet. Odds given: {}, Expected min odds: {}".format(score, betMGM_score_odds[score]['odds'], calculated_min_odds))
                to_return[score] = {"given_odds": betMGM_score_odds[score]['odds'], "calculated_odds": calculated_min_odds, "given_probability": bookie_percentage_likelihood, "calculated_probability": calculated_likelihood}
            # else:
            #     print("{}) Should NOT bet. Odds given: {}, Expected min odds: {}".format(score, betMGM_score_odds[score]['odds'], calculated_min_odds))

        return to_return


    """
    Prints and returns list of squares that are profitable to bet on
    """
    def analyze_squares(self):
        score_probabilities, squares_probabilities = self.get_heatmap_likelihoods()
        self.print_heatmap_likelihoods(score_probabilities, squares_probabilities)


        # bovada_squares_odds = self.utils.read_json(self.bovada_odds_json_path)['odds']
        # bet_MGM_score_odds = bookie_odds
        caesars_square_odds = self.caesars.get_odds()


        print("Squares odds:")
        to_return = {}
        for row in squares_probabilities:
            score = row['score']

            if score not in caesars_square_odds:
                # print("Score {} isn't available for betting in betMGM".format(score))
                continue

            bookie_percentage_likelihood = self.utils.get_percentage_likelihood_from_odds(caesars_square_odds[score]['odds'])
            calculated_likelihood = row['probability']
            calculated_min_odds = self.utils.get_odds_from_percentage_likelihood(row['probability'])

            if bookie_percentage_likelihood < calculated_likelihood:
                print("{}) Odds given: {}, Projected odds: {}".format(score, caesars_square_odds[score]['odds'], calculated_min_odds))
                to_return[score] = {"given_odds": caesars_square_odds[score]['odds'], "calculated_odds": calculated_min_odds, "given_probability": bookie_percentage_likelihood, "calculated_probability": calculated_likelihood}

        return to_return


    """
    Reads scores from heatmap_data.json, and determines which are most likely. 
    Returns two lists
        one for list of most likely actual score combinations.
        one for list of most likely squares score combinations. 
    """
    def get_heatmap_likelihoods(self):
        data = self.utils.read_json(self.heatmap_path)

        overall_score_heatmap = {}
        squares_heatmap = {}

        total_games = 0
        for row in data['matrix']:
            for item in row:
                if item['count'] > 0:
                    score_str = self.utils.score_to_str(item['pts_lose'], item['pts_win'])
                    overall_score_heatmap[score_str] = item['count']

                    score_str2 = self.utils.score_to_str(item['pts_win'], item['pts_lose'])
                    overall_score_heatmap[score_str2] = item['count']


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


    def get_frequency_likelihoods(self):
        data = self.utils.read_csv(self.frequency_path)
        del data[0] #Removes header row

        overall_score_heatmap = {}

        total_games = 0
        for row in data:
            score = row[1]
            num_games = int(row[6])

            score_str = score.replace("-", ",")

            overall_score_heatmap[score_str] = num_games
            total_games += num_games

        sorted_heatmap = dict(sorted(overall_score_heatmap.items(), key=lambda item: item[1], reverse=True))

        to_return_heatmap = []
        for score in sorted_heatmap:
            to_return_heatmap.append({"score": score, "count": sorted_heatmap[score], "probability": sorted_heatmap[score]/total_games})

        for obj in to_return_heatmap:
            print(obj)

        return to_return_heatmap


    """
    Compares probabilities calculated from heatmap data and score frequency data. They should somewhat match. 
    """
    def compare_heatmap_and_frequency(self):

        score_heatmap_probabilities, _ = self.get_heatmap_likelihoods()
        score_frequency_probabilities = self.get_frequency_likelihoods()


        self.print_heatmap_likelihoods(score_heatmap_probabilities[:30], sorted_square_heatmap=None)
        print()
        print()
        self.print_heatmap_likelihoods(score_frequency_probabilities[:30], sorted_square_heatmap=None)

        """
        20,17) 282, 1.6226480234766096%
        27,24) 230, 1.3234363312043271%
        17,14) 200, 1.1508142010472409%
        23,20) 199, 1.1450601300420047%
        24,17) 173, 0.9954542839058633%
        13,10) 167, 0.9609298578744463%
        24,21) 156, 0.897635076816848%
        17,10) 144, 0.8285862247540134%
        16,13) 143, 0.8228321537487773%
        24,14) 139, 0.7998158697278324%
        24,10) 134, 0.7710455147016514%
        23,17) 126, 0.7250129466597618%
        27,20) 125, 0.7192588756545256%
        27,17) 121, 0.6962425916335808%
        """


    """
    Prints out results of calculated sorted list of score likelihoods
    """
    def print_heatmap_likelihoods(self, sorted_heatmap=None, sorted_square_heatmap=None):
        def print_score_probabilities(heatmap_probabilities):
            for row in heatmap_probabilities:
                print("{}) {}, {}%".format(row['score'], row['count'], row['probability']*100))

        if sorted_heatmap != None:
            print("Score heatmap sorted by count:")
            print_score_probabilities(sorted_heatmap)
        print()
        if sorted_square_heatmap != None:
            print("Square game heatmap sorted by count:")
            print_score_probabilities(sorted_square_heatmap)
        print()
        # print("Total games: {}".format(total_games))
        # print()




if __name__=="__main__":
    analyzer = AnalyzeHeatmap_2023()
    # analyzer.analyze_exact_scores()
    # analyzer.analyze_squares()
    analyzer.compare_heatmap_and_frequency()