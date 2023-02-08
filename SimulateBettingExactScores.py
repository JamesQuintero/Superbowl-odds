import json
import os
import random

from Utils import Utils
from AnalyzeHeatmap_2023 import AnalyzeHeatmap_2023

"""
Simulates betting on score squares that are considered to be profitable against the odds, 
    and return profitability estimate based on different beeting strategies
"""
class SimulateBetting:

    analyzer = None
    utils = None

    def __init__(self):
        self.analyzer = AnalyzeHeatmap_2023()
        self.utils = Utils()
        self.load()

    """
    Loads probabilities
    """
    def load(self):
        #Loads best scores to bet on
        self.scores_best_odds = self.analyzer.analyze_exact_scores()
        self.squares_best_odds = self.analyzer.analyze_squares()

        #Loads calculated odds
        raw_scores_all_odds, raw_squares_all_odds = self.analyzer.get_heatmap_likelihoods()
        self.scores_all_odds = { row['score']: {"probability": row['probability'], "given_odds": self.utils.get_odds_from_percentage_likelihood(row['probability'])} for row in raw_scores_all_odds }
        self.squares_all_odds = { row['score']: {"probability": row['probability'], "given_odds": self.utils.get_odds_from_percentage_likelihood(row['probability'])} for row in raw_squares_all_odds }

        #Loads bookie odds
        self.betMGM_score_odds = self.analyzer.betMGM.get_odds()
        self.caesars_score_odds = self.analyzer.caesars.get_odds()



    def simulate_static_bet(self):

        #Goes through each line and bets $1 on each score
        base_bet_amount = 5.6
        total_bet_per_round = 0
        bets = {}
        for score in self.betMGM_score_odds:
            # bet_amount = self.utils.get_amount_to_bet(base_bet_amount, self.scores_best_odds[score]['given_odds'], self.scores_best_odds[score]['calculated_odds'])
            bet_amount = base_bet_amount
            bets[score] = bet_amount

            total_bet_per_round += bet_amount

        print()
        print("Total bet per round: ${}".format(total_bet_per_round))

        self.simulate(self.scores_all_odds, bets, total_bet_per_round, self.betMGM_score_odds)

        self.print_amount_bet_per_score(self.scores_best_odds, self.betMGM_score_odds, base_bet_amount)


    """
    Simulate betting on absolute scores that are expected to be profitable given the heatmap and odds
    """
    def simulate_profitable_bets(self):

        #Goes through each line and bets $1 on each score
        base_bet_amount = 1
        total_bet_per_round = 0
        bets = {}
        for score in self.scores_best_odds:
            bet_amount = self.utils.get_amount_to_bet(base_bet_amount, self.scores_best_odds[score]['given_odds'], self.scores_best_odds[score]['calculated_odds'])
            bets[score] = bet_amount

            total_bet_per_round += bet_amount

        print()
        print("Total bet per round: ${}".format(total_bet_per_round))

        self.simulate(self.scores_all_odds, bets, total_bet_per_round, self.betMGM_score_odds)

        self.print_amount_bet_per_score(self.scores_best_odds, self.betMGM_score_odds, base_bet_amount)



    def simulate_squares(self):
        #Goes through each line and bets $1 on each score
        base_bet_amount = 1
        total_bet_per_round = 0
        bets = {}
        for score in self.squares_best_odds:
            bet_amount = self.utils.get_amount_to_bet(base_bet_amount, self.squares_best_odds[score]['given_odds'], self.squares_best_odds[score]['calculated_odds'])
            bets[score] = bet_amount

            total_bet_per_round += bet_amount

        print()
        print("Total bet per round: ${}".format(total_bet_per_round))
        num_runs = 10000000

        simulated_squares = self.utils.get_simulated_squares(self.scores_all_odds, num_runs=num_runs)

        self.simulate(simulated_squares, self.squares_all_odds, bets, total_bet_per_round, bookie_odds=self.caesars_score_odds, num_runs=num_runs)

        self.print_amount_bet_per_score(self.squares_best_odds, self.caesars_score_odds, base_bet_amount)


    """
    Given the odds

    scores_all_odds:      Dictionary containing the probability of each score. Key is the score in string format. 
    bets:                 Dictionary of $ amount bet for each score bet on. Key is the score in string format.
    total_bet_per_round:  Total $ amount of bets.
    bookie_odds:          Dictionary of odds bookie provides and the odds you can bet on. Key is the score in string format.
    """
    def simulate(self, simulated_scores, scores_all_odds, bets, total_bet_per_round, bookie_odds, num_runs=1000000):

        #Runs 10,000,000 times
        # num_runs = 10000000

        # simulated_scores = self.utils.get_simulated_scores(scores_all_odds, num_runs)

        #Checks simulated score distributions
        simulated_scores_frequency = {}
        for score in simulated_scores:
            if score not in simulated_scores_frequency:
                simulated_scores_frequency[score] = 0 
            simulated_scores_frequency[score] += 1
        sorted_simulated_scores = dict(sorted(simulated_scores_frequency.items(), key=lambda item: item[1], reverse=True))
        sorted_simulated_scores = [ score for score in sorted_simulated_scores ]
        sorted_all_scores = [ score for score in scores_all_odds ]
        #Compare distribution of simulated scores with distribution of probaility scores, and fail if they doin't match. 
        # if set(sorted_simulated_scores[:min(10, len(sorted_simulated_scores))]) != set(sorted_all_scores[:min(10, len(sorted_all_scores))]):
        #     print("Error, distribution of simulated scores does not match distrubition of actual score probability. Try increasing num_runs.")
        #     print("Simulated scores distribution: {}".format(sorted_simulated_scores[:min(10, len(sorted_simulated_scores))]))
        #     print("Actual scores distribution: {}".format(sorted_all_scores[:min(10, len(sorted_all_scores))]))
        #     return


        total_bets = 0
        total_won = 0
        total_profitable_runs = 0
        for x in range(0, num_runs):
            if x % int(num_runs/10) == 0:
                print("{:,}/{:,}".format(x, num_runs))

            total_bets += total_bet_per_round

            score = simulated_scores[x]
            if score in bets:
                # print("Score: {}, amount_bet: {}, bookie odds: {}".format(score, bets[score], bookie_odds[score]['odds']))
                amount_won = self.utils.get_amount_won(bets[score], bookie_odds[score]['odds'])
                total_won += amount_won
                total_profitable_runs += 1
            else:
                amount_won = 0

            # print("Amount won: {}. Amount bet: {}".format(amount_won, total_bet_per_round))


        print("--- Results ---")
        print("Total bets made: ${}".format(total_bets))
        print("Total money won: ${}".format(total_won))
        print("Average bets per game: ${}".format(total_bets / num_runs))
        print("Average wins per game: ${}".format(total_won / num_runs))
        print("Profitbility %: {}%".format(((total_won / total_bets)-1)*100))
        print("Average win: ${}".format(total_won / total_profitable_runs))
        print("% runs profitable: {}%".format(total_profitable_runs / num_runs * 100))


    """
    scores_best_odds:  Dictionary of scores and their probabilities. Keys are score in string format.
    bookie_odds:       Dictionary of odds bookie provides and the odds you can bet on. Key is the score in string format.
    base_bet_amount:   $ amount of minimum bet, and each bet increases above this depending on difference between expected likelihood and bookie odds. 
    """
    def print_amount_bet_per_score(self, scores_best_odds, bookie_odds, base_bet_amount):
        print()
        print()
        print("Amount you should bet on certain scores.")
        print("Base amount: ${}".format(base_bet_amount))
        for score in scores_best_odds:
            print("{}): ${}".format(bookie_odds[score]['name'], self.utils.get_amount_to_bet(base_bet_amount, scores_best_odds[score]['given_odds'], scores_best_odds[score]['calculated_odds'])))
        print()



if __name__=="__main__":
    simulator = SimulateBetting()
    # simulator.simulate_static_bet()
    # simulator.simulate_profitable_bets()
    simulator.simulate_squares()