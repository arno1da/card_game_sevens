import unittest
from gameInstance import NewDeck


class subFunctionIntegrationTest(unittest.TestCase):

	def test_determinePlayChoices(self):
		testCase_1 = ['3c', '4c']
		trick = ['Tc']

		choices = newDeck.determinePlayChoices(testCase_1, trick, '9c')
		self.assertEqual(choices, testCase_1)

		testCase_2 = ['3c', '4d']
		choices = newDeck.determinePlayChoices(testCase_2, trick, 'Td')
		self.assertEqual(choices, ['4d'])

		testCase_3 = []
		choices = newDeck.determinePlayChoices(testCase_3, trick, '10d')
		self.assertEqual(choices, [])

	def test_determineWinner(self):

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

		testCase_1 = [
		{
			"player": 1
			,"card": '3h'
		}

		, {
			"player": 2
			,"card": '4c'
		}

		, {
			"player": 3
			,"card": 'Ac'
		}
		]

		winner = newDeck.determineWinner(testCase_1, 'As', cardRanks)

		self.assertEqual(winner, {
			"player": 1
			,"card": '3h'
		})

		testCase_2 = [
		{
			"player": 1
			,"card": '3h'
		}

		, {
			"player": 2
			,"card": '4c'
		}

		, {
			"player": 3
			,"card": 'Ah'
		}
		]

		winner = newDeck.determineWinner(testCase_2, 'As', cardRanks)

		self.assertEqual(winner, {
			"player": 3
			,"card": 'Ah'
		})

		testCase_3 = [
		{
			"player": 1
			,"card": '3h'
		}

		, {
			"player": 2
			,"card": '3s'
		}

		, {
			"player": 3
			,"card": '2s'
		}
		]

		winner = newDeck.determineWinner(testCase_3, 'As', cardRanks)

		self.assertEqual(winner, {
			"player": 2
			,"card": '3s'
		})




if __name__ == '__main__':

	def basicBidStrategy(currentBids, cards, trick):
		return 0

	def basicPlayStrategy(roundResults, cards, trick, playerChoices):
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

	unittest.main()