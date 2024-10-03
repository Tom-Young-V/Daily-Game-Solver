from words import words, weird, deluxeWords
from time import time
import re
import sys

words.extend(weird)

class WaffleSolver():
	def __init__(self, grid, size):
		self.possibleSolutions = []
		self.validSolutions = []
		self.size = size

		if size == "daily":
			self.conversions = {
				(2, 0): ((0, 0), (1, 0), (3, 0), (4, 0), (2, 1), (2, 2), (2, 3), (2, 4)),
				(0, 2): ((0, 0), (0, 1), (1, 2), (2, 2), (3, 2), (4, 2), (0, 3), (0, 4)),
				(4, 2): ((4, 0), (4, 1), (0, 2), (1, 2), (2, 2), (3, 2), (4, 3), (4, 4)),
				(2, 4): ((2, 0), (2, 1), (2, 2), (2, 3), (0, 4), (1, 4), (3, 4), (4, 4))
					}
			self.words = words
			self.amountWords = 6

		elif size == "deluxe":
			self.conversions = {

				}

			self.words = deluxeWords
			self.amountWords = 8

		self.board = Board(grid, size, self.amountWords)
		self.getPossibleWordsLists()  # gets a self.possibleWordsLists variable for optimization

		self.allSwaps = []  # [[((swapIndex1), (swapIndex2)), ... ], ... ]
		self.swaps = []
		self.nextSwaps = {}  # {simpleGrid: ((swapIndex1), (swapIndex2)), ... 
		self.terminateSwaps = False

		self.failed = False


	def getPossibleWordsLists(self):
		self.possibleWordsLists = []
		for word in range(self.amountWords):
			self.possibleWordsLists.append(self.board.getPossibleWords(word, self.words, True))


	def specialMin(self, allPossibleWords):
		started = False
		for x, row in enumerate(allPossibleWords):
			if not row:
				continue  # already solved this row

			if not started:
				minValue = (len(row), x)
				started = True

			else:
				if (newValue := len(row)) < minValue[0]:
					minValue = (newValue, x)

		return minValue[1]


	def partialSolve(self, board):
		# find the minimum of the directions left of the words
		# if there are no words:
		# return False
		# make a copy of the board
		# input the word
		# if there are no directions left:
		# return board
		# recurse

		# Find the next word to go to (the minimum of the directions left of the words)
		allPossibleWords = []

		for wordIndex in range(self.amountWords):

			if board.solvedDirections[wordIndex]:
				allPossibleWords.append(0)
				continue  # already inputted the word

			possibleWords = board.getPossibleWords(wordIndex, self.possibleWordsLists[wordIndex])

			if not len(possibleWords):
				return False  # no solutions

			allPossibleWords.append(possibleWords)


		nextWord = self.specialMin(allPossibleWords)

		board.solvedDirections[nextWord] = True

		for possibleWord in allPossibleWords[nextWord]:
			testBoard = board.copy()
			testBoard.inputWord(possibleWord, nextWord)

			if all(testBoard.solvedDirections):
				self.possibleSolutions.append(testBoard)

			else:  # continue the recursion
				self.partialSolve(testBoard)


	def checkIntersectionYellow(self, letter, wordIndex, solution):
		# get the gridline, and check that the letter is in the word, but not at the same index
		originalWord = self.board.getGridLine(wordIndex)
		solutionWordSimple = [letterInfo[0] for letterInfo in solution.getGridLine(wordIndex)]

		for x, checkLetter in enumerate(solutionWordSimple):
			if originalWord[x][1] > 1:
				continue

			if checkLetter == letter:
				return True

		return False


	def findValidSolutions(self):
		self.partialSolve(self.board)

		self.intersectionYellows = {}

		for y in range(0, len(self.board.grid), 2):
			row = self.board.grid[y]

			for x in range(0, len(row), 2):
				letterInfo = row[x]

				if letterInfo[1] != 1:
					continue

				self.intersectionYellows[(x, y)] = letterInfo[0]

		for solution in self.possibleSolutions:
			for intersection, letter in self.intersectionYellows.items():
				x, y = intersection

				# check the horizontal word
				if self.checkIntersectionYellow(letter, y // 2, solution):
					continue

				# check the vertical word
				if self.checkIntersectionYellow(letter, x // 2 + self.amountWords // 2, solution):
					continue

				# otherwise, this is not a solution
				break

			else:
				self.validSolutions.append(solution)


	def getSwapsPartial(self, board, swaps = []):
		if self.terminateSwaps:
			return

		swapped = False
		for y, row in enumerate(board.grid):
			if swapped:
				break

			for x, letterInfo in enumerate(row):
				if letterInfo[1] > 1:
					continue

				# swap the letters in the testBoard

				finalLetter = self.solution.grid[y][x][0]

				spots = board.findAll(finalLetter)
				for n, spot in enumerate(spots):

					testBoard = board.copy()
					testSwaps = swaps.copy()

					testSwaps.append(((x, y), (spot)))

					if letterInfo[0] == self.solution.grid[spot[1]][spot[0]][0]:
						testBoard.grid[spot[1]][spot[0]] = (letterInfo[0], 2)

					else:
						testBoard.grid[spot[1]][spot[0]] = (letterInfo[0], 0)  # might not be accurate, but that does not matter

					testBoard.grid[y][x] = (finalLetter, 2)

					self.getSwapsPartial(testBoard, testSwaps)

				swapped = True
				break

		if not swapped:
			self.allSwaps.append(swaps)

			if self.swapsLeft:
				if self.size == "daily" and self.swapsLeft - len(swaps) == 5 or self.size == "deluxe" and self.swapsLeft - len(swaps) == 5:
					self.terminateSwaps = True
			
			return


	def getSwaps(self):
		self.board.getUnusedLocations()
		self.getSwapsPartial(self.board)

		self.swaps = min(self.allSwaps, key = lambda x: len(x))

		# create a dictionary of {simpleGrid: nextSwap ... }

		testBoard = self.board.copy()
		for swap in self.swaps:
			self.nextSwaps[testBoard.getSimpleGrid()] = swap
			testBoard.grid[swap[0][1]][swap[0][0]], testBoard.grid[swap[1][1]][swap[1][0]] = testBoard.grid[swap[1][1]][swap[1][0]], testBoard.grid[swap[0][1]][swap[0][0]]


	def solve(self, printSolve = False, swapsLeft = False):

		self.swapsLeft = swapsLeft

		if printSolve:
			self.board.printGrid()

		self.findValidSolutions()

		if len(self.validSolutions) > 1:
			if printSolve:
				print("Failed, found multiple solutions")
				for solution in self.validSolutions:
					solution.printGrid()
			self.failed = "Error: Multiple Solutions"
			return

		if not len(self.validSolutions):
			if printSolve:
				print("Failed, found no solutions")
			self.failed = "Error: No Solutions"
			return

		self.solution = self.validSolutions[0]
		self.simpleSolution = self.solution.getSimpleGrid()

		if printSolve:
			print("Solution:")
			self.solution.printGrid()

		self.getSwaps()

		if printSolve:
			print(f"The solution takes {len(self.swaps)} swaps\n")
			for grid, swap in self.nextSwaps.items():
				self.printSimpleGrid(grid)
				print(swap)
			self.solution.printGrid()


	def printSimpleGrid(self, simpleGrid):
		print()
		for row in simpleGrid:
			for char in row:
				print(char.upper(), end = " ")
			print()
		print()


class Board():
	def __init__(self, grid, size, amountWords, directions = False):
		self.grid = grid
		self.size = size
		self.amountWords = amountWords

		if directions:
			self.solvedDirections = directions
		else:
			self.solvedDirections = [False for _ in range(amountWords)]

		self.getUnusedLetters()

	def getUnusedLetters(self):
		self.unusedLetters = []
		for row in self.grid:
			for letterInfo in row:
				if letterInfo[1] < 2:
					self.unusedLetters.append(letterInfo[0])


	def getUnusedLocations(self):
		self.unusedLocations = []
		for y, row in enumerate(self.grid):
			for x, letterInfo in enumerate(row):
				if letterInfo[1] < 2:
					self.unusedLocations.append((x, y))


	def getGridLine(self, wordIndex):
		if wordIndex < self.amountWords // 2:
			gridLine = self.grid[wordIndex * 2]
		else:
			gridLine = [row[(wordIndex - self.amountWords // 2) * 2] for row in self.grid]

		return gridLine


	def findAll(self, letter):
		spots = []
		for y, row in enumerate(self.grid):
			for x, letterInfo in enumerate(row):
				if letterInfo[1] > 1:
					continue

				if letterInfo[0] == letter:
					spots.append((x, y))

		return spots


	def specialFind(self, letter):
		for y, row in enumerate(self.grid):
			for x, letterInfo in enumerate(row):
				if letterInfo[1] > 1:
					continue

				if letterInfo[0] == letter:
					return (x, y)


	def getPossibleWords(self, wordIndex, possibleWordsList, firstTime = False):
		gridLine = self.getGridLine(wordIndex)

		pattern = ""
		otherLetters = "".join(set(self.unusedLetters))
		addedSpots = []
		for x, letterInfo in enumerate(gridLine):
			if letterInfo[1] == 2:
				pattern += letterInfo[0]
			else:
				addedSpots.append(x)
				pattern += f"[{otherLetters}]"

		testWords = [word for word in possibleWordsList if re.search(pattern, word)]
		finalWords = []

		for word in testWords:
			addedLetters = [word[x] for x in addedSpots]

			# check if the regex found words using more of a letter than it should have

			for char in addedLetters:
				if addedLetters.count(char) > self.unusedLetters.count(char):
					break

			else:
				finalWords.append(word)

		if not firstTime:
			return finalWords

		return self.firstTimeWordsFilter(finalWords, gridLine, addedSpots)


	def firstTimeWordsFilter(self, testWords, gridLine, addedSpots):
		# check if the word accounts for the original yellows and grays in the word

		# this code only needs to run the first time this function is called: when the grid is gathering the better lists of possible words
		# since the better lists will already guarantee that the yellows are correct

		# AKA: handles all the edge cases

		finalWords = []
		grays = {}
		allYellows = {}  # includes the intersection yellows for the purpose of determining what type of gray the grays are
		yellows = {}  # includes only yellows relevant to the word

		for x, letterInfo in enumerate(gridLine):
			if letterInfo[1] > 1:
				continue

			if letterInfo[1] == 0:
				if letterInfo[0] in grays:
					grays[letterInfo[0]].append(x)
				else:
					grays[letterInfo[0]] = [x]
				continue

			if letterInfo[0] in allYellows:
				allYellows[letterInfo[0]].append(x)
			else:
				allYellows[letterInfo[0]] = [x]

			if not x % 2:  # it is at an intersection of two words
				continue

			# add it to the yellows dict

			if letterInfo[0] in yellows:
				yellows[letterInfo[0]].append(x)
			else:
				yellows[letterInfo[0]] = [x]

		for word in testWords:
			stop = False

			addedLetters = [word[x] for x in addedSpots]

			for gray, spots in grays.items():
				if gray in allYellows:  # the letter could be in the added letters of the word word, just not at that spot
										# you can assume that there is no more than the len(allYellows[letter]) of the letter,
										# because if there was, the letter would be yellow

					if len(allYellows[gray]) < addedLetters.count(gray):
						stop = True
						break

					for spot in spots:
						if word[spot] == gray:
							stop = True
							break

					if stop:
						break

				else:  # the letter cannot be in the added letters of the word
					if gray in addedLetters:
						stop = True
						break

			if stop:
				continue


			# make sure the new letter is not in the same index of any of the yellows
			for yellow, yellowIndexes in allYellows.items():
				for index in yellowIndexes:
					if word[index] == yellow:
						stop = True
						break

			if stop:
				continue

			for yellow, yellowIndexes in yellows.items():
				if yellow in grays:  # there is an exact number of yellows, since there is a gray as well
					if len(yellowIndexes) != addedLetters.count(yellow):
						stop = True
						break

				if len(yellowIndexes) > addedLetters.count(yellow):  # why not len(allYellows[yellow]) > addedLetters.count(yellow)
					stop = True
					break  # the yellow was not added / not enough yellows were added


			if not stop:
				finalWords.append(word)

		return finalWords


	def inputWord(self, word, wordIndex):
		# input the word into the (nextWord) row in the grid and return a grid object

		gridLine = self.getGridLine(wordIndex)

		for n, letterInfo in enumerate(gridLine):
			if letterInfo[1] == 2:
				continue

			letter = word[n]
			x, y = self.specialFind(letter)
			if wordIndex < self.amountWords // 2:
				self.grid[2 * wordIndex][n], self.grid[y][x] = self.grid[y][x], self.grid[2 * wordIndex][n]
				self.grid[2 * wordIndex][n] = (self.grid[2 * wordIndex][n][0], 2)
			else:
				self.grid[n][2 * (wordIndex - self.amountWords // 2)], self.grid[y][x] = self.grid[y][x], self.grid[n][2 * (wordIndex - self.amountWords // 2)]
				self.grid[n][2 * (wordIndex - self.amountWords // 2)] = (self.grid[n][2 * (wordIndex - self.amountWords // 2)][0], 2)

		self.getUnusedLetters()


	def getSimpleGrid(self):
		# returns a grid of just characters, no info about color
		simpleGrid = []
		for row in self.grid:
			simpleGrid.append(tuple([letterInfo[0] for letterInfo in row]))

		return tuple(simpleGrid)


	def copy(self):
		return Board([row[:] for row in self.grid], self.size, self.amountWords, self.solvedDirections.copy())


	def printGrid(self):
		print()
		for row in self.grid:
			for letter in row:
				print(letter[0].upper(), end = " ")
			print()
		print()


if __name__ == "__main__":
	sys.path.append('./Waffle Web Scraping')
	from waffleScraping import getDaily, getDeluxe

	try:
		onlineGrids = {"daily": getDaily(), "deluxe": getDeluxe()}
		worked = True

	except:
		print("Failed to connect")
		worked = False


	if worked:
		for size, grid in onlineGrids.items():
			solver = WaffleSolver(grid, size)
			if size == "daily":
				swapsLeft = 15
			else:
				swapsLeft = 25
			solver.solve(True, swapsLeft)









