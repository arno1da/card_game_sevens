import random
import itertools

# hand = random.sample(self.deck, 5)

class newDeck(object):
	def __init__(self, players):
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
			, "trick": 'None'
			, "name": 'No trick round'

		  }
		  , {
			"cards": 7
			, "trick": 'faceDown'
			, "name": 'Face down trick round'

		  }
		  , {
			"cards": 7
			, "trick": 'allBlind'
			, "name" : "blind betting round"

		  }
		]
		pass

	def deal(cards, trick=None):
		pass

	def runIteration(position, playerTree):
		pass

	def runGame(self, roundsLeft, players):
		pass

if __name__ == "__main__":
	pass