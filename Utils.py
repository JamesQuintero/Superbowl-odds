import json
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

    Returns: dictionary
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
    Dumps data into json file to be located at path
    Returns: Boolean
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