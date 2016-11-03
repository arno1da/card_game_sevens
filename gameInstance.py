import random
from itertools import product, cycle
from pprint import pprint
from functools import reduce
from copy import deepcopy
# import functools

# hand = random.sample(self.deck, 5)

#Start simulation with two players

class NewDeck(object):
	def __init__(self, players, playerStrategies):
		self.playerStrategies = playerStrategies
		self.players = players
		self.suits = 'cdhs'
		self.ranks = '23456789TJQKA'
		self.cardRanks = {
			 "2": 1
			,"3": 2
			,"4": 3
			,"5": 4
			,"6": 5
			,"7": 6
			,"8": 7
			,"9": 8
			,"T": 9
			,"J": 10
			,"Q": 11
			,"K": 12
			,"A": 13
		}
		self.deck = tuple(''.join(card) for card in product(self.ranks, self.suits))

		self.rounds = [
		  {
		  	"cards": 1
		  	, "trick": 'faceup'
		  	, "name": 'first round'
		  }
		, {
			"cards": 2
			, "trick": 'faceup'
			, "name": 'second round'
		  }
		 , {
			"cards": 3
			, "trick": 'faceup'
			, "name" : 'third round'

		  }
		  , {
			"cards": 4
			, "trick": 'faceup'
			, "name": 'fourth round'

		  }
		  , {
			"cards": 5
			, "trick": 'faceup'
			, "name" : 'fifth round'

		  }
		  , {
			"cards": 6
			, "trick": 'faceup'
			, "name" : 'sixth round'

		  }
		  , {
			"cards": 7
			, "trick": 'faceup'
			, "name": 'seventh round'

		  }
		]

		self.scoreCard = self.generateScoreCard(players)
		self.dealerGenerator = cycle(self.scoreCard.keys())
		pass

	def generateScoreCard(self, players):
		scoreCard = {}
		for player in range(players):
			scoreCard[player + 1] = {
				"score": []
				,"roundsWon": []
			}
		return scoreCard

	def calculateScore(self, bidResults, roundResults, scoreCard, gameRound):
		for player in bidResults:
			bid = bidResults[player]
			#If player has won the amount of bids he selected he scores
			if bid == len(roundResults[player]):
				roundTotal = 10 + (2*len(roundResults[player]))
				scoreCard[player]["score"].append(roundTotal)
				scoreCard[player]["roundsWon"].append({
						"gameRound": gameRound
						,"roundResults": roundResults
						,"bidResults": bidResults
					})
			else:
				scoreCard[player]["score"].append(0)
		return scoreCard

	def drawCards(self, cards):
		return random.sample(self.deck, cards)

	def popCards(self, cardsPerHand, cardSample):
		hand = []
		for i in range(cardsPerHand):
			hand.append(cardSample.pop())
		return hand

	def dealHand(self, gameRound, players):
		boardState = {}
		if (gameRound['trick'] == 'faceup'):
			cardSample = self.drawCards(gameRound['cards'] * int(players) + 1)
			boardState['trick'] = cardSample.pop()
		else:
			cardSample = self.drawCards(gameRound['cards'] * int(players))

		for i in range(players):
			boardState[i + 1] = self.popCards(gameRound['cards'], cardSample)

		return boardState

	#Generator returning the players turn.
	def turnCycle(self,playerList, startingPoint):
		while True:
			yield playerList[startingPoint]
			startingPoint = (startingPoint + 1) % len(playerList)

	'''During the bidding round each player can bid as much as possible
	however the final player can not bid such that the sum of the previous
	bids is equal to amount of cards in each players hand. (note all players will have
	the same amount of cards)
	'''
	def submitBids(self, bidResults, dealer, turnCycle, playersStrategies, boardState, maximumDealerBid):
		playersTurn = next(turnCycle)
		strategyResult = playersStrategies[playersTurn]['bid'](bidResults, boardState[playersTurn], boardState['trick'])
		if (playersTurn == dealer):
			allCurrentBidsArray = map(lambda x: bidResults[x], list(bidResults.keys()))
			currentTotalBids = reduce(lambda x, y: x + y , allCurrentBidsArray)
			if (strategyResult + currentTotalBids) == maximumDealerBid:
				print("[ERROR]: Invalid strategy bid result. Will default to +1 above maximum")
				bidResults[playersTurn] = maximumDealerBid - currentTotalBids + 2
				#Should default to +1 for action.
			else:
				bidResults[playersTurn] = strategyResult
			return bidResults;
		else:
			bidResults[playersTurn] = strategyResult
			return self.submitBids(bidResults, dealer, turnCycle, playersStrategies, boardState, maximumDealerBid)

	def determinePlayChoices(self, cards, trick, leadingCard=None):
		if not leadingCard:
			return deepcopy(cards)
		else:
			sameSuit = filter(lambda x: (x[-1] == leadingCard[-1]) and x, cards)
			if (len(sameSuit) == 0):
				return deepcopy(cards)
			else:
				return sameSuit

	def determineWinner(self, stack, trick, cardRanks):
		playedTricks = filter(lambda x: trick[-1] == x["card"][-1] and x, stack)
		if (len(playedTricks) > 0):
			highestTrick = reduce(lambda x, y: cardRanks[x["card"][0]] < cardRanks[y["card"][0]] and y or x , playedTricks)
			return highestTrick
		else:
			leadingCard = stack[0]["card"]
			def compareCards(x, y):
				if (y["card"][-1] == leadingCard[-1] and (cardRanks[x["card"][0]] < cardRanks[y["card"][0]])):
					return y
				else:
					return x
			highestLeadingCardSuit = reduce(compareCards, stack)
			return highestLeadingCardSuit

	def playoutRound(self, currentHandStack, roundResults, playersStrategies, boardState, turnCycle, leadingPlayer=None):
		currentPlayer = next(turnCycle)
		if not leadingPlayer:
			leadingPlayer = currentPlayer

		if len(currentHandStack) == 0:
			playerChoices = self.determinePlayChoices(boardState[currentPlayer], boardState['trick'])
		else:
			playerChoices = self.determinePlayChoices(boardState[currentPlayer], boardState['trick'], currentHandStack[0]["card"])

		if len(playerChoices) == 1:
			playedCard = playerChoices[0]
		else:
			playedCard = playersStrategies[currentPlayer]['play'](roundResults, boardState[currentPlayer], boardState['trick'], playerChoices, currentHandStack)
			if (playedCard not in playerChoices):
				playedCard = playerChoices[0]

		currentHandStack.append({
			"player": currentPlayer
			, "card": playedCard})
		boardState[currentPlayer].remove(playedCard)

		#If current player is the player to the right of the starting player we have finished our round.
		if (currentPlayer == ((leadingPlayer + (len(playersStrategies.keys()) - 1)) % len(playersStrategies.keys()))):
			#If we have no cards left the game is over
			if len(boardState[currentPlayer]) == 0:
				winningPlay = self.determineWinner(currentHandStack, boardState['trick'], self.cardRanks)
				roundResults[winningPlay["player"]].append(currentHandStack)
				return roundResults
			else:
				winningPlay = self.determineWinner(currentHandStack, boardState['trick'], self.cardRanks)
				roundResults[winningPlay["player"]].append(currentHandStack)
				#Start round with empty stack
				currentHandStack = []
				return self.playoutRound(currentHandStack, roundResults, playersStrategies, boardState, turnCycle)
		else:
			#we need to continue the round
			return self.playoutRound(currentHandStack, roundResults , playersStrategies, boardState, turnCycle, leadingPlayer)

	def runGame(self, roundsLeft, players, scoreCard):
		if len(roundsLeft) == 0:
			return scoreCard
		gameRound = roundsLeft.pop(0)
		print(self.players)
		print("about to start game round")
		print(gameRound)
		dealer = next(self.dealerGenerator)
		print("here is our dealer")
		print(dealer)

		boardState = self.dealHand(gameRound, players)
		print("here is our board state")
		print(boardState)

		#List starting with index 0 shift the entire list by 1.
		newBetGenerator = self.turnCycle(list(self.scoreCard.keys()), ((dealer + 1) % len(self.scoreCard.keys())) - 1)

		maximumDealerBid = gameRound["cards"]
		bidResults = self.submitBids({}, dealer, newBetGenerator, self.playerStrategies, boardState, maximumDealerBid)
		print("here are our bid results")
		print(bidResults)

		#create another generator set
		turnCycle = self.turnCycle(list(self.scoreCard.keys()), ((dealer + 1) % len(self.scoreCard.keys())) - 1)

		roundResults = {}
		for i in self.scoreCard.keys():
			roundResults[i] = []

		roundResults = self.playoutRound([], roundResults , self.playerStrategies, boardState, turnCycle)
		print("here are our round results!")
		print(roundResults)

		scoreCard = self.calculateScore(bidResults, roundResults, scoreCard, gameRound)

		return self.runGame(roundsLeft, players, scoreCard)


	def initiateGame(self):
		gameScore = self.runGame(self.rounds, self.players, self.scoreCard)
		print("here is our final game score!")
		pprint(gameScore)



if __name__ == "__main__":
	def basicStrategy(cards, players, scoreCard):
		return

	def basicBidStrategy(currentBids, cards, trick):
		return 1

	def basicPlayStrategy(roundResults, cards, trick, playerChoices, currentRoundStack):
		print("this is the current round stack")
		print(currentRoundStack)
		print("here is our player choices")
		print(roundResults)
		print(playerChoices)
		print(cards)
		print(trick)
		cardRanks = {
			 "2": 1
			,"3": 2
			,"4": 3
			,"5": 4
			,"6": 5
			,"7": 6
			,"8": 7
			,"9": 8
			,"T": 9
			,"J": 10
			,"Q": 11
			,"K": 12
			,"A": 13
		}

		def compareCards(x, y):
			if ((cardRanks[x[0]] < cardRanks[y[0]])):
				return y
			else:
				return x
		highestChoice = reduce(compareCards , playerChoices)

		print("this is our highestChoice")
		print(highestChoice)
		return highestChoice


	newDeck = NewDeck(
		players=3
		, playerStrategies={
			1: {
				"bid": basicBidStrategy,
				"play": basicPlayStrategy
			},

			2: {
				"bid": basicBidStrategy,
				"play": basicPlayStrategy
			},

			3: {
				"bid": basicBidStrategy,
				"play": basicPlayStrategy
			}
		}
		)
	newDeck.initiateGame()
	pass