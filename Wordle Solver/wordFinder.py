import re
from words import words, weird
import random

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

class WordFinder():
	def __init__(self):
		self.usableLetters = alphabet.copy()
		self.possibleWords = words


	def getColoredLists(self, guess):
		lists = [{}, {}, {}]  # grays, yellows, greens

		for x, letterInfo in enumerate(guess):
			letter, color = letterInfo

			colorList = lists[color]

			if letter in colorList:
				colorList[letter].append(x)
			else:
				colorList[letter] = [x]

			if letter in self.usableLetters:
				otherSpots = [letterInfo[1] for letterInfo in guess if letterInfo[0] == letter]
				if not any(otherSpots):
					self.usableLetters.remove(letter)

		return lists

	def getPossibleWords(self, guess):
		grayList, yellowList, greenList = self.getColoredLists(guess)

		pattern = [f"[{''.join(self.usableLetters)}]" for _ in range(5)]
		for letter, locations in greenList.items():
			for location in locations:
				pattern[location] = letter

		pattern = "".join(pattern)
		possibleWords = [word for word in self.possibleWords if re.search(pattern, word)]

		finalWords = []

		for word in possibleWords:
			stop = False

			# grays

			for grayLetter, spots in grayList.items():
				for spot in spots:
					if word[spot] == grayLetter:
						stop = True
						break

				if stop:
					break

				if grayLetter in yellowList or grayLetter in greenList:  # then it could be in the word, but an exact amount
					totalInWord = 0
					for colorList in [yellowList, greenList]:
						if grayLetter in colorList:
							totalInWord += len(colorList[grayLetter])

					if word.count(grayLetter) != totalInWord:
						stop = True
						break

				else:  # then the letter is not in the word
					if grayLetter in word:
						stop = True
						break

			if stop:
				continue

			# yellows

			for yellowLetter, spots in yellowList.items():
				for spot in spots:
					if word[spot] == yellowLetter:
						stop = True
						break

				if stop:
					break

				if len(spots) > word.count(yellowLetter):
					stop = True
					break

				# yellow being in grays, and needing to be counted exactly is already accounted for

			if not stop:
				finalWords.append(word)

		self.possibleWords = finalWords


	def rankWords(self):
		# rank words based on which one narrows down the search the most
		return random.choice(self.possibleWords)


testGuesses = [
	[("s", 0), ("a", 0), ("l", 1), ("e", 1), ("t", 0)],
	[("e", 1), ("l", 2), ("e", 0), ("g", 0), ("y", 0)]
		]

solver = WordFinder()
for guess in testGuesses:
	solver.addGuess(guess)

print(solver.possibleWords)
# print(solver.rankWords())










