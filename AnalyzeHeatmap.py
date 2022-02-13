import json
import os


class AnalyzeHeatmap:

    bovada_odds_txt_path = "./data/2022/Bovada_odds.txt"
    bovada_odds_json_path = "./data/2022/Bovada_odds.json"
    heatmap_path = "./data/2022/heatmap_data.json"
    teams_playing = ["team1", "team2"]

    def __init__(self):
        pass


    """
    Prints and returns list of scores that are profitable to bet on
    """
    def analyze(self):
        score_probabilities, squares_probabilities = self.get_heatmap_likelihoods()
        self.print_heatmap_likelihoods(score_probabilities, squares_probabilities)


        bovada_squares_odds = self.read_json(self.bovada_odds_json_path)['odds']

        print("Squares odds:")
        to_return = {}
        for row in squares_probabilities:
            score = row['score']
            bookie_percentage_likelihood = self.get_percentage_likelihood_from_odds(bovada_squares_odds[score])
            calculated_likelihood = row['probability']
            calculated_min_odds = self.get_odds_from_percentage_likelihood(row['probability'])

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
                    score_str = self.score_to_str(item['pts_lose'], item['pts_win'])
                    overall_score_heatmap[score_str] = item['count']


                    squares_score_str = self.score_to_str(item['pts_lose']%10, item['pts_win']%10)
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




    """
    Returns percentage likelihood that the odds corresponds to. 
    EX: 2500 odds corresponds to 0.0385 likelihood
    """
    def get_percentage_likelihood_from_odds(self, odds):
        if odds > 0:
            return 100 / (odds + 100)
        else:
            return (-1*(odds)) / (-1(odds) + 100)

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
    Assumes Bovada odds data in Bovada_odds.txt is in format
        Rams 0 Bengals 0 +3500
        Rams 1 Bengals 0 +6600
        Rams 2 Bengals 0 +10000
    """
    def transform_bovada_odds(self):

        if os.path.isfile(self.bovada_odds_json_path):
            print("Bovada odds already exist in {}".format(self.bovada_odds_json_path))
            return

        odds_txt = self.read_from_txt(self.bovada_odds_txt_path)

        favored_team = -1
        
        to_save = {}
        to_save['teams'] = []
        to_save['odds'] = {}
        for row in odds_txt:
            split_row = row.split(" ")

            if favored_team == -1:
                favored_team = self.ask_team_odds(split_row[0], split_row[2])

            if favored_team == 0:
                score = self.score_to_str(split_row[3], split_row[1])
                to_save['teams'] = [split_row[2], split_row[0]]
            else:
                score = self.score_to_str(split_row[1], split_row[3])
                to_save['teams'] = [split_row[0], split_row[2]]

            to_save['odds'][score] = int(split_row[4].replace("+", ""))

        self.save_to_json(self.bovada_odds_json_path, to_save)

    """
    Determines who is the favored team to know how to sort the bovada odds when converting from txt to json.
    """
    def ask_team_odds(self, team1, team2):
        choice = -1
        while choice != 1 and choice != 2:
            print("Teams playing: ")
            print("1) {}".format(team1))
            print("2) {}".format(team2))
            choice = int(input("Who has better odds of winning? (Team with minus/negative odds): "))

        return choice - 1

        # print("Look at Win odds for each team. (ex: -190 for favorable team)")
        # input("Odds for {} to win: ".format(team1))
        # input("Odds for {} to win: ".format(team2))
        # return 





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




if __name__=="__main__":
    analyzer = AnalyzeHeatmap()
    analyzer.transform_bovada_odds()
    analyzer.analyze()