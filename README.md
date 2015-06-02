ECHESS, Chess Move-Evaluation for ranking players
======

Studies have been done by chess researchers to address concerns by the Chess community regarding the incapacity of the Elo rating approach to accurate determine the relative skill of players in different leagues and in different eras. These studies proposed a chess skill rating system which uses chess engines run to high depth, so that their playing strength far exceeds that of the best human chess player, as a benchmark against which the quality of moves played is judged. The majority of these studies however, were unable to address the issue of statistical confidence. This CLI tool addresses this issue by providing a scalable infrastructure aimed at analyzing bulk collections of games by players across different chess federations and eras. With the help of top UCI chess engines, we can quickly analyze millions of chess games in PGN format. A database of the analyzed games can hence be used by chess researches to study player performances on a large scale with statistical confidence.
