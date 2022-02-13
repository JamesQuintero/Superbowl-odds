# Superbowl score betting

### How it works
Sports bookies gives odds and allow betting on the superbowl game ending on certain scores, like 35-42, but Bovada is doing the Squares game instead. So take the last digit of each score and that'll correspond to a square. The 35-42 score will be considered 5,2, and you can bet on that score combination along with 100 or so others. This program uses a heatmap of all professional american football scores over the past 80 years or so to determine which square is most likely to come up, and will say to bet on certain squares if the likelihood is better than the odds Bovada gives.

For example, bookie might give odds of +2500 for square 7,0, meaning they think final score ending in 7-0 has a 3.85% chance of occuring. But historical scores might show that score has a 5% chance of occuring (+1900). It'll be profitable to bet on that score if the odds given are >+1900, and they are.


### Data

#### Heatmap data
Heatmap data is downloaded from https://nflscorigami.com/data. Copy paste all into the heatmap_data.json file.

#### Odds data

Bovada odds are copy pasted from their site into a txt file where the rows are the format

```
Rams 0 Bengals 0 +3500
Rams 1 Bengals 0 +6600
Rams 2 Bengals 0 +10000
...
```

AnalyzerHeatmap then transforms this into json data and saves to Bovada_odds.json. These odds are read during the actual run of the program so that only profitable bets are displayed. 


