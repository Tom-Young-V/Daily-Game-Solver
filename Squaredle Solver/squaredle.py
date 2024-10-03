from grid import Grid
from allwords import allwords

board = "golbaloebnazsany"
wordSize = 4

printSolve = True

grid = Grid(board, wordSize, printSolve, debugMode = True)
print(len(grid.letters), grid.gridSize)
grid.findAllWords()

print(sorted(grid.words, key = lambda w: len(w))[::-1])

