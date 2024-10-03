from wordleSolver import WordleSolver
from time import perf_counter, sleep
from words import words
from random import sample
from collections import defaultdict
from bestBeginningWords import firstWordValues
from bestBeginningWordsV2 import firstWordValuesV2
from math import floor


def getAverageGuesses(guessesData):
	totalWords = sum([amount for amount in guessesData.values()])
	averageAmountGuesses = 0
	for amountGuesses, total in guessesData.items():
		averageAmountGuesses += amountGuesses * total / totalWords
	return averageAmountGuesses

# percentList = [231, 463, 694, 926, 1157, 1389, 1620, 1852, 2083, 2315]
def testSolver(startingWord, repetitions, printSolve):
	if repetitions == -1:
		solutionWords = words
	else:
		solutionWords = sample(words, repetitions)
	amountWords = len(solutionWords)

	wordSolvingData = {}
	guessesData = defaultdict(int)
	timeSpentData = []

	for x, solutionWord in enumerate(solutionWords):
		if printSolve:
			if not x % 100 and x != 0:
				print(f"Over {x + 1} / {len(solutionWords)} trials ({(x + 1) / len(solutionWords):.2%} complete) the solver took on average:")
				print(f"{getAverageGuesses(guessesData):.2f} guesses and {sum(timeSpentData) / len(timeSpentData):.2f} seconds per solve")
				print(f"Spent {sum(timeSpentData):.2f} seconds so far, estimated time remaining: {(sum(timeSpentData) / len(timeSpentData) * (len(solutionWords) - (x + 1))) / 60:.2f} minutes\n")

		# if (x + 1) in percentList:
		# 	print(f"{(percentList.index((x + 1)) + 1) / len(percentList):.0%}")


		startTime = perf_counter()

		solver = WordleSolver(startingWord = startingWord)
		amountGuesses = solver.solve(solutionWord)

		timeSpent = perf_counter() - startTime

		wordSolvingData[solutionWord] = (amountGuesses, timeSpent)
		guessesData[amountGuesses] += 1
		timeSpentData.append(timeSpent)

		if printSolve:
			print(f"Solved {solutionWord} in {amountGuesses} guesses taking {timeSpent:.2f} seconds")
			print(f"Used words {[guess[0] for guess in solver.guesses]}")
			print("\n\n")

	print(f"On average, the solver took {getAverageGuesses(guessesData):.4f} guesses and {sum(timeSpentData) / len(timeSpentData):.4f} seconds per solve")
	return sorted(guessesData.items())


def getFirstWordValuesWithLookAhead():
	solver = WordleSolver()

	firstWordValuesV2 = {}
	wordsToCheck = 100

	for x, (word, expectedValue) in enumerate(firstWordValues[-wordsToCheck:]):
		print(f"Looking two words ahead for {word} with an initial expected value of {expectedValue:.4f}")
		startTime = perf_counter()
		oneAheadValue, twoAheadValue = solver.getNarrowingFactor(word, lookTwoAhead = True)
		totalTime = perf_counter() - startTime
		firstWordValuesV2[word] = (oneAheadValue, twoAheadValue, oneAheadValue + twoAheadValue)
		print(f"Found that the average expected value for a following word is {twoAheadValue:.4f}, giving {word} a total value of {oneAheadValue + twoAheadValue}")
		print(f"Took {totalTime:.4f} seconds {(x + 1) / wordsToCheck:.2%} done\n")


	print(sorted(firstWordValuesV2.items(), key = lambda x: x[1][2]))


def getBestSecondWords(word):
	startTime = perf_counter()
	solver = WordleSolver()

	bestSecondWords = {}

	for colors, words in solver.getPossibleOutcomes(word).items():
		solver = WordleSolver()
		solver.inputWord(word, colors)

		bestSecondWords[colors] = solver.rank()

	totalTime = perf_counter() - startTime

	return bestSecondWords


def getAllBestSecondWords():
	allBestSecondWords = {}

	timing = []
	for x, (word, expectedValues) in enumerate(firstWordValuesV2):
		startTime = perf_counter()
		allBestSecondWords[word] = getBestSecondWords(word)
		totalTime = perf_counter() - startTime
		timing.append(totalTime)

		estimatedTimeRemaining = sum(timing) / len(timing) * (len(firstWordValuesV2) - (x + 1))
		estimatedTimeRemaining = f"{estimatedTimeRemaining / 60:.2f} minutes"

		print(f"Finished with {word}, {(x + 1) / len(firstWordValuesV2):.2%} complete. Estimated time remaining: {estimatedTimeRemaining}\n")

	print(allBestSecondWords)


def timeString(seconds):
	if seconds >= 3600:
		hours = f"{seconds // 3600:.0f} hours, "
		seconds = seconds % 3600
	else:
		hours = ""

	if seconds >= 60:
		minutes = f"{seconds // 60:.0f} minutes, "
		seconds = seconds % 60
	else:
		minutes = ""

	seconds = f"{seconds / 1:.2f} seconds"

	return f"{hours}{minutes}{seconds}"


def testBestWords():
	totalWordValues = {}

	timing = []

	for x, (word, expectedValues) in enumerate(firstWordValuesV2):
		startTime = perf_counter()
		startingWord = (word, expectedValues[0])

		print(f"Testing solver with starting word {startingWord}")
		
		totalWordValues[word] = testSolver(startingWord, -1, False)
		totalTime = perf_counter() - startTime

		timing.append(totalTime)

		print(f"Spent {timeString(sum(timing))}. Estimated time remaining: {timeString(sum(timing) / len(timing) * (len(firstWordValuesV2) - (x + 1)))}\n")

	print(totalWordValues)

testBestWords()






