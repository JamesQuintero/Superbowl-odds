# Results


## Superbowl LVI 2022
Bovada.lv provides better opportunities for squares game, where the last digit of the score points to a coordinate on a grid and you can bet on points on that grid. Certain scores and their score combinations are more likly than others, so it's prudent to figure out the likelihood of each square, the odds Bovada provides to bet on it, and whether it's profitable to place that bet. 


## Live betting results:
Bets placed: 
| Bet placed | Amount $ | Won amount |
| ---------- | ---------- | ---------- |
|  |  |  |



## Actual bets placed: 
```
Amount you should bet on certain scores. Bengals vs Rams
7,0): $5.875820895522388
0,7): $5.615319148936169
0,3): $7.273181126331811
0,4): $8.099130434782609
0,0): $7.212713178294573
7,1): $17.507967479674797
0,1): $22.31478260869565
7,7): $10.139600886917961
3,4): $25.318949880668256
0,6): $6.174736842105262
7,8): $28.576374269005846
6,7): $9.66440251572327
4,4): $31.77777777777778
0,8): $28.57964912280702
4,8): $19.08463768115942
7,5): $29.701747572815535
0,5): $13.081025641025638
0,2): $10.706236559139786
4,5): $18.85221556886227
7,2): $8.762816901408454
3,5): $9.736470588235292
```


## Betting simulation: 

### If we made a $1 bet on all possible squares no matter the probability

```
Total bet per round: $100
Gathering 10,000,000 scores...
0/10,000,000
1,000,000/10,000,000
2,000,000/10,000,000
3,000,000/10,000,000
4,000,000/10,000,000
5,000,000/10,000,000
6,000,000/10,000,000
7,000,000/10,000,000
8,000,000/10,000,000
9,000,000/10,000,000
--- Results ---
Total bets made: $1000000000
Total money won: $677400606.0
Average bets per game: $100.0
Average wins per game: $67.7400606
Profitbility %: -32.25993940000001%
Average win: $67.7400606
% runs profitable: 100.0%
```

We would be betting on every square Bovada provides, and we would be guaranteed to lose 32% of our total bet. 


### If we made a $1 bet on squares that come up more often than Bovada thinks
```
Total bet per round: $21
Gathering 10,000,000 scores...
0/10,000,000
1,000,000/10,000,000
2,000,000/10,000,000
3,000,000/10,000,000
4,000,000/10,000,000
5,000,000/10,000,000
6,000,000/10,000,000
7,000,000/10,000,000
8,000,000/10,000,000
9,000,000/10,000,000
--- Results ---
Total bets made: $210000000
Total money won: $278940853.0
Average bets per game: $21.0
Average wins per game: $27.8940853
Profitbility %: 32.82897761904762%
Average win: $60.37151570046349
% runs profitable: 46.20405%
```

We whould only bet on squares that we believe have a higher probabilty of occuring than Bovada's odds indicate. 54% of the time we wouldn't win anything, but when we do win, we'd average 300% for an average profit of 33% of our bet for every game.

### If we bet more if there's a bigger difference between actual probability and Bovada predictions

```
Total bet per round: $57.86706369283747
Gathering 10,000,000 scores...
0/10,000,000
1,000,000/10,000,000
2,000,000/10,000,000
3,000,000/10,000,000
4,000,000/10,000,000
5,000,000/10,000,000
6,000,000/10,000,000
7,000,000/10,000,000
8,000,000/10,000,000
9,000,000/10,000,000
--- Results ---
Total bets made: $578670636.9424182
Total money won: $862599366.6960593
Average bets per game: $57.86706369424182
Average wins per game: $86.25993666960593
Profitbility %: 49.065688083616045%
Average win: $186.71030459301178
% runs profitable: 46.19988%
```

We whould only bet on squares that we believe have a higher probabilty of occuring than Bovada's odds indicate. 54% of the time we wouldn't win anything, just like the previous simulation, but when we do win, we'd average >300% for an average profit of 49% of our bet for every game. So the strategy of increasing the bet size for squares where there's an even great discrepancy between our calculated odds and Bovada's odds, give the biggest profit.
