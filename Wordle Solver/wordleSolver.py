from words import words as usableWords, weird
import random
from collections import defaultdict
from math import log2
from bestBeginningWordsV2 import bestFirstWordV2, bestSecondWordsV2
from time import perf_counter
	
# start = perf_counter()
# from colorsTable import colorsTable
# print(f"Loaded colorsTable, took {perf_counter() - start:.2f} seconds\n")

allWords = usableWords.copy()
allWords.extend(weird)

class WordleSolver():
	def __init__(self, startingWord = False, onlySimpleWords = False):
		self.possibleWords = usableWords.copy()
		self.amountPossibleWords = len(self.possibleWords)
		self.guesses = []

		if startingWord:
			self.startingWord = startingWord
		else:
			self.startingWord = bestFirstWordV2

		self.onlySimpleWords = onlySimpleWords


	def getColors(self, guessWord, possibleWord):

		try:
			return colorsTable[(guessWord, possibleWord)]
		except:
			pass  # colorsTable not imported

		# finds the colors of guessWord if possibleWord were to be the solution

		colors = [3 for _ in range(5)]  # list of numbers (0 - gray, 1 - yellow, 2 - green)
		accountedLetters = defaultdict(int)

		# greens / grays - you have to do these first for the logic between yellows and grays
		for x, letter in enumerate(guessWord):
			if letter not in possibleWord:
				colors[x] = 0

			elif letter == possibleWord[x]:
				colors[x] = 2
				accountedLetters[letter] += 1

		# yellow / grays
		for x, letter in enumerate(guessWord):
			if colors[x] != 3:
				continue

			# the letter must be in the word, but could be either yellow or green

			if letter in accountedLetters:
				amountAccounted = accountedLetters[letter]
			else:
				amountAccounted = 0

			if possibleWord.count(letter) - amountAccounted > 0:
				accountedLetters[letter] += 1
				colors[x] = 1
			else:
				colors[x] = 0

		return tuple(colors)


	def getPossibleOutcomes(self, guessWord):
		possibleOutcomes = defaultdict(list)

		for possibleWord in self.possibleWords:
			possibleOutcomes[self.getColors(guessWord, possibleWord)].append(possibleWord)

		return possibleOutcomes


	def bitFormula(self, amountMatches):
		return log2(self.amountPossibleWords / amountMatches)


	def getNarrowingFactor(self, guessWord, lookTwoAhead = False, printSolve = False):
		factor = 0

		if lookTwoAhead:
			twoAheadFactor = 0

		outComes = self.getPossibleOutcomes(guessWord).items()

		amountPossibleOutcomes = len(outComes)

		for x, (colors, words) in enumerate(sorted(outComes)):
			amountMatches = len(words)
			probability = amountMatches / len(self.possibleWords)

			factor += probability * self.bitFormula(amountMatches)

			if lookTwoAhead:
				solver = WordleSolver()
				solver.inputWord(guessWord, colors)

				bestNextWord, expectedValue = solver.rank()
				twoAheadFactor += probability * expectedValue

				if printSolve:
					print(f"With colors {colors} {probability:.2%}, the best next word is {bestNextWord} with an expected value of {expectedValue:.2f}, {x / amountPossibleOutcomes:.2%} done")

		if lookTwoAhead:
			return (factor, twoAheadFactor)

		else:
			return factor


	def rank(self, lookTwoAhead = False):
		if self.onlySimpleWords:
			wordsList = usableWords
		else:
			wordsList = allWords

		wordValues = {}
		for word in wordsList:
			wordValues[word] = self.getNarrowingFactor(word, lookTwoAhead)

		bestNextWord = max(wordValues, key = wordValues.get)

		for word in self.possibleWords:
			if wordValues[word] == wordValues[bestNextWord]:
				return (word, wordValues[word])

		return max(wordValues.items(), key = lambda x: x[1])


	def inputWord(self, guessWord, colors):
		self.possibleWords = self.getPossibleOutcomes(guessWord)[colors]
		self.amountPossibleWords = len(self.possibleWords)
		self.guesses.append((guessWord, colors))


	def inputWordManual(self, guessWord, colors):
		expectedValue = self.getNarrowingFactor(guessWord)
		print(f"Inputting '{guessWord}' for an expected value of {expectedValue:.2f}\n")

		value = self.bitFormula(len(self.getPossibleOutcomes(guessWord)[colors]))
		print(f"Got the combination {colors}, giving a value of {value:.2f}\n")

		self.possibleWords = self.getPossibleOutcomes(guessWord)[colors]
		self.amountPossibleWords = len(self.possibleWords)
		self.guesses.append((guessWord, colors))

		print(f"Narrowed it down to {self.amountPossibleWords}:\n\n{self.possibleWords}")
		print(f"{[f'{self.getNarrowingFactor(word):.3f}' for word in self.possibleWords]}\n\n")

		suggestedWord, expectedValue = self.rank()

		print(f"Suggested next guesses: {suggestedWord}, giving a value of {expectedValue:.2f}\n")


	def solve(self, solutionWord, printSolve = False):
		for x in range(12):
			if not self.onlySimpleWords:

				if not x:
					bestNextWord, expectedValue = self.startingWord

				elif x == 1 and self.guesses[0][0] in bestSecondWordsV2:
					bestNextWord, expectedValue = bestSecondWordsV2[self.guesses[0][0]][self.guesses[0][1]]

				else:
					bestNextWord, expectedValue = self.rank()

			else:
				bestNextWord, expectedValue = self.rank()



			if printSolve:
				print(f"Inputting '{bestNextWord}' for an expected value of {expectedValue:.2f}")

			if printSolve:
				colors = self.getColors(bestNextWord, solutionWord)
				value = self.bitFormula(len(self.getPossibleOutcomes(bestNextWord)[colors]))
				print(f"Got the combination {colors}, giving a value of {value:.2f}")


			colors = self.getColors(bestNextWord, solutionWord)
			self.inputWord(bestNextWord, colors)

			if bestNextWord == solutionWord:
				if printSolve:
					print(f"Found the solution in {x + 1} guesses")
				return x + 1

			if printSolve:
				print(f"Narrowed it down to {self.amountPossibleWords}:\n{self.possibleWords}")
				print("\n\n")

		else:
			return "More than 12"


if __name__ == "__main__":

	if True:
		solver = WordleSolver()

		guesses = {
			"salet": (0, 0, 0, 1, 0),
			"drone": (0, 1, 0, 1, 1)
				}

		for guess, colors in guesses.items():
			solver.inputWordManual(guess, colors)

	if False:
		solver = WordleSolver()

		solution = "lanky"  # random.choice(usableWords)
		print(f"{solution}\n")

		solver.solve(solution, True)









