# Superbowl score betting

### How it works
Sports bookies gives odds and allow betting on the superbowl game ending on certain scores, like 35-42, but for the 2022 Superbowl, Bovada is doing the Squares game instead. So take the last digit of each score and that'll correspond to a square. The 35-42 score will be considered 5,2, and you can bet on that score combination along with 100 or so others. This program uses a heatmap of all professional american football scores over the past 80 years or so to determine which square is most likely to come up, and will say to bet on certain squares if the likelihood is better than the odds Bovada gives.

For example, bookie might give odds of +2500 for square 7,0, meaning they think final score ending in 7-0 has a 3.85% chance of occuring. But historical scores might show that score has a 5% chance of occuring (+1900). It'll be profitable to bet on that score if the odds given are >+1900, and they are.


Unfortunately for 2023 Superbowl, Bovada is doing absolute final score, like 35-42. This is similar to vegas bookies, like BetMGM. But BetMGM gives better odds for the scores. 

### [See results for Superbowl LVI 2022](./results.md)
### [See results for Superbowl LVII 2023](./data/2023/results.md)


### Data

[Info](./data_download.md) on how to download the proper data