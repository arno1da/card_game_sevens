import random
import itertools

# hand = random.sample(self.deck, 5)

#Start simulation with two players

class newDeck(object):
	def __init__(self, players, strategyDict):
		self.players = players
		self.suits = 'cdhs'
		self.ranks = '23456789TJQKA'
		self.deck = tuple(''.join(card) for card in itertools.product(self.ranks, self.suits))

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
		 , {
			"cards": 3
			, "trick": 'faceup'
			, "name" : 'third round'

		  }
		]
		pass

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

	'''During the bidding round each player can bid as much as possible
	however the final player can not bid such that the sum of the previous
	bids is equal to amount of cards in each players hand. (note all players will have
	the same amount of cards)
	'''
	def biddingRound(self, choices, cards):
		pass

	def runGame(self, roundsLeft, players, scoreCard):
		if len(roundsLeft) == 0:
			return scoreCard
		gameRound = roundsLeft.pop(0)


		pass

if __name__ == "__main__":
	pass