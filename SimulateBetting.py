import json
import os
import random

from AnalyzeHeatmap import AnalyzeHeatmap

"""
Simulates betting on score squares that are considered to be profitable against the odds, 
    and return profitability estimate based on different beeting strategies
"""
class SimulateBetting:

    squares_best_odds = {}
    squares_all_odds = {}
    analyzer = None

    def __init__(self):
        self.analyzer = AnalyzeHeatmap()
        self.load()

    """
    Loads probabilities
    """
    def load(self):
        self.analyzer.transform_bovada_odds()

        #Loads calculated odds
        self.squares_best_odds = self.analyzer.analyze()
        _, raw_squares_all_odds = self.analyzer.get_heatmap_likelihoods()
        self.squares_all_odds = { row['score']: {"probability": row['probability'], "given_odds": self.analyzer.get_odds_from_percentage_likelihood(row['probability'])} for row in raw_squares_all_odds }

        #Loads bookie (Bovada) odds
        bovada_squares = self.analyzer.read_json(self.analyzer.bovada_odds_json_path)
        self.teams_playing = bovada_squares['teams']
        self.bovada_squares_odds = bovada_squares['odds']



    def simulate(self):

        #Goes through each line and bets $1 on each score
        base_bet_amount = 5.6
        total_bet_per_round = 0
        bets = {}
        for score in self.squares_all_odds:
            # bet_amount = self.get_amount_to_bet(base_bet_amount, self.squares_all_odds[score]['given_odds'], self.squares_all_odds[score]['calculated_odds'])
            bet_amount = 1
            bets[score] = bet_amount

            total_bet_per_round += bet_amount

        print()
        print("Total bet per round: ${}".format(total_bet_per_round))

        #Runs 10,000,000 times
        num_runs = 10000000

        simulated_scores = self.get_simulated_scores(num_runs)

        #Checks simulated score distributions
        simulated_scores_frequency = {}
        for score in simulated_scores:
            if score not in simulated_scores_frequency:
                simulated_scores_frequency[score] = 0 
            simulated_scores_frequency[score] += 1
        sorted_simulated_scores = dict(sorted(simulated_scores_frequency.items(), key=lambda item: item[1], reverse=True))
        sorted_simulated_scores = [ score for score in sorted_simulated_scores ]
        sorted_squares_all_scores = [ score for score in self.squares_all_odds ]
        #Compare distribution of simulated scores with distribution of probaility scores, and fail if they doin't match. 
        if sorted_simulated_scores[:min(10, len(sorted_simulated_scores))] != sorted_squares_all_scores[:min(10, len(sorted_squares_all_scores))]:
            print("Error, distribution of simulated scores does not match distrubition of actual score probability. Try increasing num_runs.")
            print("Simulated scores distribution: {}".format(sorted_simulated_scores[:min(10, len(sorted_simulated_scores))]))
            print("Actual scores distribution: {}".format(sorted_squares_all_scores[:min(10, len(sorted_squares_all_scores))]))
            return

        total_bets = 0
        total_won = 0
        total_profitable_runs = 0
        for x in range(0, num_runs):
            if x % int(num_runs/10) == 0:
                print("{:,}/{:,}".format(x, num_runs))

            total_bets += total_bet_per_round

            score = simulated_scores[x]
            if score in self.squares_all_odds:
                amount_won = self.get_amount_won(bets[score], self.bovada_squares_odds[score])
                # print("Amount won: {}. Amount bet: {}".format(amount_won, total_bet_per_round))
                total_won += amount_won
                total_profitable_runs += 1


        print("--- Results ---")
        print("Total bets made: ${}".format(total_bets))
        print("Total money won: ${}".format(total_won))
        print("Average bets per game: ${}".format(total_bets / num_runs))
        print("Average wins per game: ${}".format(total_won / num_runs))
        print("Profitbility %: {}%".format(((total_won / total_bets)-1)*100))
        print("Average win: ${}".format(total_won / total_profitable_runs))
        print("% runs profitable: {}%".format(total_profitable_runs / num_runs * 100))

        print()
        print()
        print("Amount you should bet on certain scores. {} vs {}".format(self.teams_playing[0], self.teams_playing[1]))
        for score in self.squares_all_odds:
            print("{}): ${}".format(score, self.get_amount_to_bet(base_bet_amount, self.squares_best_odds[score]['given_odds'], self.squares_best_odds[score]['calculated_odds'])))
        print()


    """ 
    Returns "optimal" amount to bet depending on difference between calculated probability of the event and odds given
    """
    def get_amount_to_bet(self, base_bet_amount, given_odds, calculated_odds):
        return base_bet_amount + base_bet_amount * ((given_odds - calculated_odds) / 1000)


    def get_simulated_scores(self, num_runs):
        print("Gathering {:,} scores...".format(num_runs))
        population = [ score for score in self.squares_all_odds ]
        weights = [ self.squares_all_odds[score]['probability']*100 for score in self.squares_all_odds ]
        return random.choices(population, weights=weights, k=num_runs)


    """
    Calculates how much won from a bet given the odds. You receive your original bet back
    """
    def get_amount_won(self, bet_amount, odds):
        if odds > 0:
            return bet_amount + bet_amount * (odds / 100)
        else:
            print("TODO: Implement calculating won amount from negative odds.")
            


        




if __name__=="__main__":
    simulator = SimulateBetting()
    simulator.simulate()