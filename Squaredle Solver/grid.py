# from wordslist import wordslist
from allwords import allwords
from wordStrand import WordStrand
from lastGrid import lastGrid
from math import sqrt
import re
import time
import os

class Grid:
	def __init__(self, letters, minimumWordSize = 4, printSolve = False, debugMode = False):
		letters = [letter.lower() for letter in letters]

		if type(letters) == str:
			letters = list(letters)  # so it can accept just a string of the letters in order for ease of typing in the grid

		self.usableLetters = set(letters)
		self.usableLettersRe = "".join(self.usableLetters)
		self.letters = letters
		self.gridSize = int(sqrt(len(letters)))
		self.wordStrands = []
		self.words = []
		self.minimumWordSize = minimumWordSize
		self.printSolve = printSolve
		self.debugMode = debugMode

		if debugMode:
			self.startTime = time.time()

		self.wordsList = allwords  # wordslist

	def getSurroundingIndexes(self, index):
		indexes = []

		# top and bottom

		if index < self.gridSize:
			top = True
		else:
			indexes.append(index - self.gridSize)
			top = False

		if index >= self.gridSize ** 2 - self.gridSize:
			bottom = True
		else:
			indexes.append(index + self.gridSize)
			bottom = False

		# left and right, along with diagonals

		if index % self.gridSize:
			indexes.append(index - 1)
			if not top:
				indexes.append(index - 1 - self.gridSize)
			if not bottom:
				indexes.append(index - 1 + self.gridSize)

		if index % self.gridSize != self.gridSize - 1:
			indexes.append(index + 1)
			if not top:
				indexes.append(index + 1 - self.gridSize)
			if not bottom:
				indexes.append(index + 1 + self.gridSize)

		return sorted(indexes)

	def testValid(self, wordStrand):
		# test if the wordStrand should be added to the list of words

		if len(wordStrand.word) >= self.minimumWordSize:
			if wordStrand.word in self.wordsList:
				if wordStrand.word not in [strand.word for strand in self.wordStrands]:  # make sure its not already in the list
					if self.printSolve:
						print(wordStrand.word)
					self.wordStrands.append(wordStrand)

					if self.debugMode:
						if len(self.wordStrands) % 50 == 0:
							print(f"Found {len(self.wordStrands)} words")


	def buildWord(self, wordStrand):
		# adds one letter to a wordStrand

		self.testValid(wordStrand)
		
		# check if there are more words to be built upon it

		pattern = f"{wordStrand.word}[{self.usableLettersRe}]+"
		wordStrand.possibleWords = [word for word in wordStrand.possibleWords if re.fullmatch(pattern, word)]

		if not wordStrand.possibleWords:
			return  # there are no more possible words on this strand

		# build on the word by going to the surrounding indexes of the current index that have not already been used

		for index in self.getSurroundingIndexes(wordStrand.currentIndex):
			if index in wordStrand.indexes:
				continue  # already used in the word

			newWordStrand = wordStrand.copy()
			newWordStrand.addLetter(index, self.letters[index])

			self.buildWord(newWordStrand)


	def findAllWords(self):

		if self.debugMode:
			print(lastGrid[0], "\n", tuple(self.letters))
			print(lastGrid[0] == tuple(self.letters))
			if lastGrid[0] == tuple(self.letters):
				self.wordStrands = [WordStrand(wordStrand[1], wordStrand[1][-1], wordStrand[0], []) for wordStrand in lastGrid[1]]
				self.words = [wordStrand.word for wordStrand in self.wordStrands]

				return self.wordStrands


		for index, letter in enumerate(self.letters):

			if self.debugMode:
				print(f"On letter {index + 1} / {len(self.letters)} ({letter}), {round(time.time() - self.startTime, 3)} seconds elapsed")

			pattern = f"{letter}[{self.usableLettersRe}]+"
			possibleWords = [word for word in self.wordsList if re.fullmatch(pattern, word)]

			wordStrand = WordStrand([index], index, letter, possibleWords)

			self.buildWord(wordStrand)

		self.words = [wordStrand.word for wordStrand in self.wordStrands]

		if self.debugMode:
			script_dir = os.path.dirname(os.path.abspath(__file__))
			
			file_path = os.path.join(script_dir, "lastGrid.py")
			
			with open(file_path, "w") as file:
				file.write(f"lastGrid = {(tuple(self.letters), tuple([(wordStrand.word, wordStrand.indexes) for wordStrand in self.wordStrands]))}\n")

		return self.wordStrands

"""
keep a list of which words have been found in the case of duplicates of the same word
keep a list of the indexes of which letters have been used in the current word so they cant go back on themselves

1	for each letter in the grid:
2		test that there are still possible words
3		get each possible direction from that letter
4		for each possible direction
5			add to the list of indexes of letters
6			if the word created is in the words list, append that word to the list of found words
			recurse steps 2 - 6
"""


