h3. Intro:

The following is a simulation of a variation of ohel. There are 10 rounds and the game is based on points and contains 'tricks'. Tricks represent the leading strongest suite and also the win of a hand. 10 Points are awarded if the player determined the amount of 'tricks' (hands won) in the betting round plus an extra 2 points per 'trick' won.

For each round there are two phases. For the first phase players take turns from the 'left' of the dealer (in the simulation case incremental player number) bidding on the amount of tricks they think they will win. With the dealer dealing last the sum of the bids can not equal the amount of cards in each players hand.

For example if it was round 2 (each player receives 2 cards) of a 3 player game and the current bids were 1 and 0 player 3 can not bid 1 as then the total bids would sum to the amount of cards. 

The next phase is the playing phase. During this phase the player who bid first will lead. The leading card's suite is the winning suite. The players will then take turns playing a single card to follow. If the player has the same suite as the leading card the player must play this suite (or a card with the same suite). This is called 'following suite'. If the player can not follow suite then any card can be played. The winner of the hand round is the player that played the highest starting suite or if tricks are present the highest trick. The player who won the round is then able to lead.

For this variation the rounds up to 7 contain incremental cards starting from 1. Round 8-10 are special rounds. Round 8 there is no trick available. For round 9 the trick is face down during the bidding round and for round 10 both the players cards and trick are unknown to them. 


h4. Functions required to enter a bot.

The game currently takes two functions your bidding strategy and play strategy. The arguments are as follows:

bidStrategy(gameRound, scoreCard, currentBids, cards, trick)

playStrategy(gameRound, scoreCard, currentRoundResults, cards, trick, playerChoices, currentRoundStack)