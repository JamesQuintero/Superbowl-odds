


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


### BetMGM odds

https://sports.ny.betmgm.com/en/sports/api/widget?layoutSize=Large&page=SportLobby&sportId=11&forceFresh=1
Or go to https://sports.ny.betmgm.com/en/sports/football-11, Use Network tab in Chrome, click on Outcome Oracle (Predict the Correct Score). Find the request titled "widget?layoutSize=Large&page=SportLobby&sportId=11&forceFresh=1". 




### Frequency data
Frequency data (game_frequency.csv) is downloaded from https://www.pro-football-reference.com/boxscores/game-scores.htm. Copy paste all into the game_frequency.csv file. 

### Heatmap data
Heatmap data (heatmap_data.json) is downloaded from https://nflscorigami.com/data. Copy paste all into the heatmap_data.json file.  