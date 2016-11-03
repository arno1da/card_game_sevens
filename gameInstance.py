import random
from itertools import product, cycle
from pprint import pprint
from functools import reduce
from copy import deepcopy

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



	def setUpGameRounds(self):
		return  [
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

		  , {
		  	"cards": 7
		  	, "trick": 'none'
		  	, "name": 'eighth round'
		  }

		  , {
		  	"cards": 7
		  	, "trick": 'blind'
		  	, "name": 'nineth round'
		  }

		  , {
		  	"cards": 7
		  	, "trick": 'blind'
		  	, "name": 'final blind round'
		  }
		]


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
			boardState['trick'] = None

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

	Information changes depending on the rounds.
	'''
	def submitBids(self, bidResults, dealer, turnCycle, playersStrategies, boardState, maximumDealerBid, gameRound):
		playersTurn = next(turnCycle)

		if (gameRound["trick"] == 'blind' or gameRound["trick"] == 'none'):
			strategyResult = playersStrategies[playersTurn]['bid'](bidResults, deepcopy(boardState[playersTurn]), None)
		elif (gameRound["name"] == "blind betting round"):
			strategyResult = playersStrategies[playersTurn]['bid'](bidResults, [], None)
		else:
			strategyResult = playersStrategies[playersTurn]['bid'](bidResults, deepcopy(boardState[playersTurn]), boardState['trick'])

		if (playersTurn == dealer):
			allCurrentBidsArray = map(lambda x: bidResults[x], list(bidResults.keys()))
			currentTotalBids = reduce(lambda x, y: x + y , allCurrentBidsArray)
			if (strategyResult + currentTotalBids) == maximumDealerBid:
				logging.info("[ERROR]: Invalid strategy bid result for player #%s. Will default to +1 above maximum" % (str(playersTurn)))
				bidResults[playersTurn] = maximumDealerBid - currentTotalBids + 2
				#Should default to +1 for action.
			else:
				bidResults[playersTurn] = strategyResult
			return bidResults;
		else:
			bidResults[playersTurn] = strategyResult
			return self.submitBids(bidResults, dealer, turnCycle, playersStrategies, boardState, maximumDealerBid, gameRound)

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
		if (trick):
			playedTricks = filter(lambda x: trick[-1] == x["card"][-1] and x, stack)
		else:
			playedTricks = []

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

	def playoutRound(self, gameRound, scoreCard, currentHandStack, roundResults, playersStrategies, boardState, turnCycle, endingPlayer=None, leadingPlayer=None):
		currentPlayer = next(turnCycle)
		if not leadingPlayer:
			leadingPlayer = currentPlayer
		if not endingPlayer:
			#rule set to have the ending player on the other end of the cycle
			if leadingPlayer == len(playersStrategies.keys()):
				endingPlayer = 1
			elif leadingPlayer == 1:
				endingPlayer = len(playersStrategies.keys())
			else:
				endingPlayer = leadingPlayer - 1

		if len(currentHandStack) == 0:
			playerChoices = self.determinePlayChoices(deepcopy(boardState[currentPlayer]), boardState['trick'])
		else:
			playerChoices = self.determinePlayChoices(deepcopy(boardState[currentPlayer]), boardState['trick'], currentHandStack[0]["card"])

		if len(playerChoices) == 1:
			playedCard = playerChoices[0]
		else:
			playedCard = playersStrategies[currentPlayer]['play'](
					gameRound, scoreCard,
					roundResults, deepcopy(boardState[currentPlayer]),
					boardState['trick'], playerChoices,
					currentHandStack
				)
			if (playedCard not in playerChoices):
				logging.info("[ERROR]: Invalid play strategy player #%s. Will default to first choice." % (str(currentPlayer)))
				playedCard = playerChoices[0]

		currentHandStack.append({
			"player": currentPlayer
			, "card": playedCard})

		boardState[currentPlayer].remove(playedCard)

		#If current player is the player to the right of the starting player we have finished our round.
		if (currentPlayer == endingPlayer):
			#If we have no cards left the game round is over
			if len(boardState[currentPlayer]) == 0:
				winningPlay = self.determineWinner(currentHandStack, boardState['trick'], self.cardRanks)
				roundResults[winningPlay["player"]].append(currentHandStack)
				return roundResults
			else:
				winningPlay = self.determineWinner(currentHandStack, boardState['trick'], self.cardRanks)
				roundResults[winningPlay["player"]].append(currentHandStack)
				#Start next play round with an empty stack
				currentHandStack = []
				return self.playoutRound(gameRound, scoreCard, currentHandStack, roundResults, playersStrategies, boardState, turnCycle, endingPlayer)
		else:
			#we need to continue the round
			return self.playoutRound(gameRound, scoreCard, currentHandStack, roundResults , playersStrategies, boardState, turnCycle, endingPlayer, leadingPlayer)

	def runGame(self, roundsLeft, players, scoreCard):
		if len(roundsLeft) == 0:
			return scoreCard
		gameRound = roundsLeft.pop(0)

		determineDealer = random.randint(0, len(list(scoreCard.keys())) -1)

		dealerGenerator = self.turnCycle(list(scoreCard.keys()), determineDealer)

		dealer = next(dealerGenerator)

		boardState = self.dealHand(gameRound, players)

		#List starting with index 0 shift the entire list by 1.
		newBetGenerator = self.turnCycle(list(scoreCard.keys()), ((dealer + 1) % len(scoreCard.keys())) - 1)
		maximumDealerBid = gameRound["cards"]
		bidResults = self.submitBids({}, dealer, newBetGenerator, self.playerStrategies, boardState, maximumDealerBid, gameRound)

		#create another generator set
		turnCycle = self.turnCycle(list(scoreCard.keys()), ((dealer + 1) % len(scoreCard.keys())) - 1)

		roundResults = {}
		for i in scoreCard.keys():
			roundResults[i] = []

		roundResults = self.playoutRound(gameRound, scoreCard, [], roundResults , self.playerStrategies, boardState, turnCycle)

		scoreCard = self.calculateScore(bidResults, roundResults, scoreCard, gameRound)

		return self.runGame(roundsLeft, players, scoreCard)

	def calculateGameWinner(self, gameScores):

		currentWinningPlayers = [{
			"score": 0
			,"player": 'invalid'
			,"totalScore": 0
		}]
		for player in gameScores.keys():
			currentPlayerScore = reduce(lambda x, y: x + y, gameScores[player]['score'])
			if (currentPlayerScore > currentWinningPlayers[0]["totalScore"]):
				currentWinningPlayers = [{"score":gameScores[player], "player": player, "totalScore": currentPlayerScore}]
			elif (currentPlayerScore == currentWinningPlayers[0]["totalScore"]):
				currentWinningPlayers.append({"score":gameScores[player], "player": player, "totalScore": currentPlayerScore})

		return currentWinningPlayers


	def initiateGame(self, gameIterations):

		totalGameWinners = {}

		for i in range(self.players):
			totalGameWinners[i + 1] = 0

		totalGameScores = {}
		for i in range(gameIterations):
			singleGameScore = self.runGame(self.setUpGameRounds(), self.players, self.generateScoreCard(self.players))
			totalGameScores['game' + str(i + 1)] = {
				"winner": self.calculateGameWinner(singleGameScore),
				"scoreSheet": singleGameScore
			}

			for winner in totalGameScores['game' + str(i + 1)]["winner"]:
				totalGameWinners[winner['player']] += 1

		# pprint("here is our total Game Scores")
		# print(totalGameScores)
		print("Final game score.")
		pprint(totalGameWinners)

	



if __name__ == "__main__":
	import logging
	logging.basicConfig(format='%(asctime)s %(message)s', filename='card_game_sevens.log', level=logging.WARNING)
	logging.propagate = False

	def basicBidStrategy(currentBids, cards, trick):
		return 1

	#Basic strategy of playing highest possible card
	def basicPlayStrategy(gameRound, scoreCard, currentRoundResults, cards, trick, playerChoices, currentRoundStack):
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

	newDeck.initiateGame(gameIterations=5)
