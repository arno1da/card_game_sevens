import random
from itertools import product, cycle
# import functools

# hand = random.sample(self.deck, 5)

#Start simulation with two players

class NewDeck(object):
	def __init__(self, players):
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
			cardSample = drawCards(gameRound['cards'] * int(players) + 1)
			boardState['trick'] = cardSample.pop()
			for i in range(players):
				boardState['player' + str(i)] = self.popCards(gameRound['cards'], cardSample)
		else:
			drawCards(gameRound['cards'] * int(players))
			for i in range(players):
				boardState['player' + str(i)] = self.popCards(gameRound['cards'], cardSample)

		return boardState

	#Generator returning the players turn.
	def turnCycle(playerList, startingPoint=None):
		startingPOint = 0 if startingPOint is None else playerList.index(startingPoint)
		while True:
			yield playerList[startingPoint]
			startingPoint = (startingPoint + 1) % len(playerList)

	def submitBids(self, bidRounds, dealer, turnCycle playersStrategies):
		playersTurn = next(turnCycle)
		if (playersTurn == dealer):
			self.submitBid(playersStrategies[dealer].bid(bidRounds), self.players, bidRounds)
			return bidRounds;
		else:
			self.submitBid(playersStrategies[playersTurn].bid(bidRounds), self.players, bidRounds)
			return submitBids(self, bidRounds, dealer, playersStrategies)


	'''During the bidding round each player can bid as much as possible
	however the final player can not bid such that the sum of the previous
	bids is equal to amount of cards in each players hand. (note all players will have
	the same amount of cards)
	'''
	def biddingRound(self, choices, cards):
		print("hurr, durr, I'm arnold")
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




	def initiateGame(self, strategy):
		self.runGame(self.rounds, self.players, self.scoreCard)
		pass

if __name__ == "__main__":
	def basicStrategy(cards, players, scoreCard):
		return 


	newDeck = NewDeck(players=2)
	newDeck.initiateGame(basicStrategy)
	pass