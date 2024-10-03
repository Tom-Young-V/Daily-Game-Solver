from wordleSolver import WordleSolver
from words import words as usableWords, weird
import pickle

allWords = usableWords.copy()
allWords.extend(weird)

solver = WordleSolver()

colorsTable = {}

for x, guessWord in enumerate(allWords):
	if not x % (len(allWords) // 100):
		print(f"{x}, {x / len(allWords):.0%}")
	for solutionWord in usableWords:
		colorsTable[(guessWord, solutionWord)] = solver.getColors(guessWord, solutionWord)

with open('colorsTable.pkl', 'wb') as file:
    pickle.dump(colorsTable, file)
