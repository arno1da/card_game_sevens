Intro:

The following is a simulation of a variation of ohel. There are 10 rounds and the game is based on points and contains 'trumps'. Trumps represent the leading strongest suite. 10 Points are awarded if the player determined the amount of 'tricks' (hands won) in the betting round plus an extra 2 points per 'trick' won.

For each round there are two phases. For the first phase players take turns from the 'left' of the dealer (in the simulation case incremental player number) bidding on the amount of tricks they think they will win. With the dealer dealing last the sum of the bids can not equal the amount of cards in each players hand.

For example if it was round 2 (each player receives 2 cards) of a 3 player game and the current bids were 1 and 0 player 3 can not bid 1 as then the total bids would sum to the amount of cards.

The next phase is the playing phase. During this phase the player who bid first will lead. The leading card's suite is the current winning suite. The players will then take turns playing a single card to follow. If the player has the same suite as the leading card the player must play this suite (or a card with the same suite in the case of multiple). This is called 'following suite'. If the player can not follow suite then any card can be played. The winner of the hand round is the player that played the highest starting suite or if trumps are present the highest trump. The player who won the trick is then able to lead until each player is no cards remaining.

For this variation the rounds up to 7 contain incremental cards starting from 1. Round 8-10 are special rounds. Round 8 there is no trick available. For round 9 the trick is face down during the bidding round and for round 10 both the players cards and trick are unknown to them.


Functions required to enter a bot.

The game currently takes two functions your bidding strategy and play strategy. The arguments are as follows:

bidStrategy(gameRound, scoreCard, currentBids, cards, trick)

playStrategy(gameRound, scoreCard, currentRoundResults, cards, trick, playerChoices, currentRoundStack)