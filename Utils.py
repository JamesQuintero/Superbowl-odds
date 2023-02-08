import json
import csv
import os


class Utils:

    """
    Returns percentage likelihood that the odds corresponds to. 
    EX: 2500 odds corresponds to 0.0385 likelihood
    """
    def get_percentage_likelihood_from_odds(self, odds):
        if odds > 0:
            return 100 / (odds + 100)
        else:
            return (-1*(odds)) / (-1*(odds) + 100)

    """
    Returns odds that the percentage liklihood corresponds to.
    EX: 0.0385 likelihood corresponds to +2500 odds
    """
    def get_odds_from_percentage_likelihood(self, probability):
        if probability < 0.5:
            return (100 / probability) - 100
        else:
            return 100 * probability / (probability - 1)


    """ 
    Returns "optimal" amount to bet depending on difference between calculated probability of the event and odds given
    """
    def get_amount_to_bet(self, base_bet_amount, given_odds, calculated_odds):
        return base_bet_amount + base_bet_amount * ((given_odds - calculated_odds) / 1000)


    """
    Calculates how much won from a bet given the odds. You receive your original bet back
    """
    def get_amount_won(self, bet_amount, odds):
        if odds > 0:
            return bet_amount + bet_amount * (odds / 100)
        else:
            print("TODO: Implement calculating won amount from negative odds.")


    """
    Returns list of simulated potential scores based on their likelihood of happening
    scores_all_odds is calculated from heatmap. 
    """
    def get_simulated_scores(self, scores_all_odds, num_runs):
        import random
        print("Gathering {:,} scores...".format(num_runs))
        population = [ score for score in scores_all_odds ]
        weights = [ scores_all_odds[score]['probability']*100 for score in scores_all_odds ]
        return random.choices(population, weights=weights, k=num_runs)


    def get_simulated_squares(self, scores_all_odds, num_runs):
        simulated_scores = self.get_simulated_scores(scores_all_odds, num_runs)
        squares = []
        for score in simulated_scores:
            score = self.str_to_score(score)
            square = [score[0]%10, score[1]%10]
            squares.append(self.score_to_str(square[0], square[1]))

        return squares


    """
    Converts [12, 35] into "12,35"
    """
    def score_to_str(self, losing_score, winning_score):
        return "{},{}".format(losing_score, winning_score)

    """
    Converts "12,35" into [12, 35]
    """
    def str_to_score(self, score_str):
        score_list = score_str.split(",")
        return [ int(score) for score in score_list]

    """
    Reads from text file, and returns list of strings that was read from text file at path

    Returns: List
    """
    def read_from_txt(self, path):
        if os.path.exists(path):
            try:
                f = open(path)
                contents = f.readlines()

                to_return = []
                for line in contents:
                    line = line.strip()
                    to_return.append(line)

                return to_return
            except Exception as error:
                print("Couldn't read file: {}".format(error))
                return []
        else:
            print("File doesn't exist: {}".format(path))
            return []

    """
    Reads json file and returns data in json format
    """
    def read_json(self, json_path):
        try:
            with open(json_path) as json_file:
                data = json.load(json_file)

                return data
        except Exception as error:
            print("Error, couldn't load json file: {}".format(error))

        return {}


    """
    Reads csv file and returns data in list format
    """
    def read_csv(self, csv_path):
        if os.path.isfile(csv_path):
            with open(csv_path, newline='') as file:
                contents = csv.reader((line.replace('\0', '') for line in file)) #replaces possible nullbytes when reading file

                temp_list=[]
                for row in contents:
                    temp_matrix=[]
                    for stuff in row:
                         temp_matrix.append(stuff)
                    temp_list.append(temp_matrix)

                return temp_list
        else:
            print("CSV at {} doesn't exist".format(csv_path))
            path = os.getcwd()
            print("Current directory: {}".format(path))
            return []

    """
    Dumps data into json file to be located at path
    """
    def save_to_json(self, path, data):
        try:
            with open(path, 'w') as outfile:
                json.dump(data, outfile, sort_keys=True, indent=4)
        except Exception as error:
            print("Error, couldn't save data to json: {}".format(error))
            return False

        return True

    """
    Determines what year of odds to use. ex: 2023
    """
    def ask_year(self):
        potential_years = os.listdir("./data")

        choice = -1
        while choice < 0 or choice > len(potential_years):
            print("Teams playing: ")
            for i, year in enumerate(potential_years):
                print("{}) {}".format(i+1, year))
            choice = int(input("Choice: "))

        return potential_years[choice - 1]