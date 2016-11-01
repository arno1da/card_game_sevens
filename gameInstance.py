import random
from itertools import product, cycle
from pprint import pprint
from functools import reduce
# import functools

# hand = random.sample(self.deck, 5)

#Start simulation with two players

class NewDeck(object):
	def __init__(self, players, playerStrategies):
		self.playerStrategies = playerStrategies
		self.players = players
		self.suits = 'cdhs'
		self.ranks = '23456789TJQKA'
		self.deck = tuple(''.join(card) for card in product(self.ranks, self.suits))

		self.rounds = [
		  {
		  	"cards": 1
		  	, "trick": 'faceUp'
		  	, "name": 'first round'
		  }
		, {
			"cards": 2
			, "trick": 'faceup'
			, "name": 'second round'
		  }
		]

		self.scoreCard = self.generateScoreCard(players)
		self.dealerGenerator = cycle(self.scoreCard.keys())
		pass

	def generateScoreCard(self, players):
		scoreCard = {}
		for player in range(players):
			scoreCard[player + 1] = []
		print("here iso ur score card")
		print(scoreCard)
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
			for i in range(players):
				boardState[i + 1] = self.popCards(gameRound['cards'], cardSample)
		else:
			cardSample = self.drawCards(gameRound['cards'] * int(players))
			for i in range(players):
				boardState[i + 1] = self.popCards(gameRound['cards'], cardSample)

		return boardState

	def submitBid(self, strategyResult, bidResults, player, maximumDealerBid, dealerIndicator=False):
		
		if dealerIndicator == True:
			allCurrentBidsArray = map(lambda x: bidResults[x], list(bidResults.keys()))
			currentTotalBids = reduce(lambda x, y: x + y , allCurrentBidsArray)
			if (strategyResult + currentTotalBids) == maximumDealerBid:
				print("[ERROR]: Invalid strategy bid result. Will default to +1 above maximum")
				bidResults[player] = maximumDealerBid - currentTotalBids + 2 
				#Should default to +1 for action.
			else:
				bidResults[player] = strategyResult
		else:
			bidResults[player] = strategyResult


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
		print("here are our bid results so far")
		print(bidResults)
		playersTurn = next(turnCycle)
		print("here is our players turn")
		print(playersTurn)
		if (playersTurn == dealer):
			self.submitBid(playersStrategies[dealer]['bid'](bidResults, boardState[dealer], boardState['trick']), bidResults, dealer, maximumDealerBid, True)
			return bidResults;
		else:
			self.submitBid(playersStrategies[playersTurn]['bid'](bidResults, boardState[playersTurn], boardState['trick']), bidResults, playersTurn, maximumDealerBid)
			return self.submitBids(bidResults, dealer, turnCycle, playersStrategies, boardState, maximumDealerBid)


	def playoutRound(self, roundResults, leadingPlayer, playerStrategies, boardState, turnCycle):


		pass


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

		boardState = self.dealHand(gameRound, self.players)
		print("here is our board state")
		print(boardState)


		#List starting with index 0 shift the entire list by 1.
		newBetGenerator = self.turnCycle(list(self.scoreCard.keys()), ((dealer + 1) % len(self.scoreCard.keys())) - 1)

		maximumDealerBid = gameRound["cards"]
		bidResults = self.submitBids({}, dealer, newBetGenerator, self.playerStrategies, boardState, maximumDealerBid)
		# roundResults = 

		#create another generator set
		leadingPlayer = self.turnCycle(list(self.scoreCard.keys()), ((dealer + 1) % len(self.scoreCard.keys())) - 1)
		print("here are our bid results")
		print(bidResults)


	def initiateGame(self):
		self.runGame(self.rounds, self.players, self.scoreCard)


if __name__ == "__main__":
	def basicStrategy(cards, players, scoreCard):
		return

	def basicBidStrategy(currentBids, cards, trick):
		print("here are our current bids")
		print(currentBids)

		print("here are our cards")
		print(cards)
		return 1

	def basicPlayStrategy():
		return


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