


### Bovada odds

Odds were selected from the webpage and copy pasted into a txt document. ex: ./data/2022/Bovada_odds.txt. 

```
Rams 0 Bengals 0 +3500
Rams 1 Bengals 0 +6600
Rams 2 Bengals 0 +10000
...
```

Run the following to convert this txt file to a usable json file. 

```
./Bovada.py 
```


Or go to https://www.bovada.lv/sports/football/super-bowl-score-propositions/, Use Network tab in Chrome. Find the request titled "score-propositions-super-bowl-57-202302121830?lang=en". 


### BetMGM odds

https://sports.ny.betmgm.com/en/sports/api/widget?layoutSize=Large&page=SportLobby&sportId=11&forceFresh=1  
Or go to https://sports.ny.betmgm.com/en/sports/football-11, Use Network tab in Chrome, click on Outcome Oracle (Predict the Correct Score). Find the request titled "widget?layoutSize=Large&page=SportLobby&sportId=11&forceFresh=1". 


### Caesar odds 

https://www.williamhill.com/us/ny/bet/api/v3/sports/americanfootball/events/futures/?competitionIds=007d7c61-07a7-4e18-bb40-15104b6eac92

Or go to Caesar's sportsbook (williamhill.com): https://www.williamhill.com/us/ny/bet/americanfootball?id=007d7c61-07a7-4e18-bb40-15104b6eac92

And open up the Network tab in your browser. Find the request "?competitionIds=XXXX-xxxx-XXXX-XxxxxX"


### Fanduel odds

Or go to Fanduel Sportsbook -> Scoring, and open up the Network tab in your browser. Find the request "event-page?betexRegion=GBR&capiJurisdiction=intl&curren...."


### Wynnbet

Wynnbet has horrible reviews and a bad UI, so will not be simulating with their odds. 

### Draftkings

https://sportsbook.draftkings.com//sites/US-SB/api/v5/eventgroups/88808/categories/528/subcategories/12130?format=json

Or go to Draftking's sportsbook -> Game Props -> Correct Score, and open up the Network tab in your browser. Find the request "12130?format=json", in which 12130 is probably an event id that will change for each subsequent super bowl. 


### BetRivers

BetRivers doesn't seem to allow betting on exact scores or squares. 


### PointsBet

PointsBet doesn't seem to allow betting on exact scores or squares.


### Unibet

Unibet doesn't seem to allow betting on exact scores or squares. 


### Frequency data
Frequency data (game_frequency.csv) is downloaded from https://www.pro-football-reference.com/boxscores/game-scores.htm. Copy paste all into the game_frequency.csv file. 

### Heatmap data
Heatmap data (heatmap_data.json) is downloaded from https://nflscorigami.com/data. Copy paste all into the heatmap_data.json file.  