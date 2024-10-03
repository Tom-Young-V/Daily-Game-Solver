from words import words, weird
import copy

words.extend(weird)

def printGrid(grid):
  print("\n")
  for i in range(5):
    print(f"{grid[i][0]} {grid[i][1]} {grid[i][2]} {grid[i][3]} {grid[i][4]}")
  print("\n")

def swapLetters(grid, index1, index2, letter):
  for i in range(5):
    for j in range(5):
      if grid[i][j] == letter:
        grid[index1][index2], grid[i][j] = grid[i][j], grid[index1][index2]
  return grid

def getUsableLetters(grid):
  usableLetters = []
  for i in range(5):
    for j in range(5):
      if grid[i][j] != " " and grid[i][j] == grid[i][j].lower():
        usableLetters.append(grid[i][j])
  return sorted(usableLetters)

def getRandomStr(grid, size):
  usableLetters = getUsableLetters(grid)
  randomStr = []
  if size == 4:
    for i in range(len(usableLetters)):
      for j in range(len(usableLetters)):
        for k in range(len(usableLetters)):
          for l in range(len(usableLetters)):
            if i != j and i != k and i != l and j != k and j != l and k != l:
              letters = [usableLetters[i], usableLetters[j], usableLetters[k], usableLetters[l]]
              str = "".join(letters)
              if str not in randomStr:
                randomStr.append("".join(letters))
  elif size == 3:
    for i in range(len(usableLetters)):
      for j in range(len(usableLetters)):
        for k in range(len(usableLetters)):
          if i != j and i != k and j != k:
            letters = [usableLetters[i], usableLetters[j], usableLetters[k]]
            str = "".join(letters)
            if str not in randomStr:
              randomStr.append("".join(letters))
  elif size == 2:
    for i in range(len(usableLetters)):
      for j in range(len(usableLetters)):
        if i != j:
          letters = [usableLetters[i], usableLetters[j]]
          str = "".join(letters)
          if str not in randomStr:
            randomStr.append("".join(letters))
  elif size == 1:
    for letter in usableLetters:
      if letter not in randomStr:
        randomStr.append(letter)
  else:
    print("Cannot find strings of size 0. Word must already be solved.")
  return randomStr

def solveWord(grid, word):
  letters = []
  count = 0
  solutions = []
  positions = []
  if word == "top":
    for i in range(5):
      if grid[0][i] != grid[0][i].lower():
        letters.append(grid[0][i])
      else:
        letters.append(0)
        count += 1
    for i in range(letters.count(0)):
      positions.append(letters.index(0))
      letters[letters.index(0)] = 1
    randomStr = getRandomStr(grid, count)
    for str in randomStr:
      for index, num in enumerate(positions):
        letters[num] = str[index]
      word = "".join(letters).lower()
      if word in words and word not in solutions:
        solutions.append(word)
  elif word == "middleAcross":
    for i in range(5):
      if grid[2][i] != grid[2][i].lower():
        letters.append(grid[2][i])
      else:
        letters.append(0)
        count += 1
    for i in range(letters.count(0)):
      positions.append(letters.index(0))
      letters[letters.index(0)] = 1
    randomStr = getRandomStr(grid, count)
    for str in randomStr:
      for index, num in enumerate(positions):
        letters[num] = str[index]
      word = "".join(letters).lower()
      if word in words and word not in solutions:
        solutions.append(word)
  elif word == "bottom":
    for i in range(5):
      if grid[4][i] != grid[4][i].lower():
        letters.append(grid[4][i])
      else:
        letters.append(0)
        count += 1
    for i in range(letters.count(0)):
      positions.append(letters.index(0))
      letters[letters.index(0)] = 1
    randomStr = getRandomStr(grid, count)
    for str in randomStr:
      for index, num in enumerate(positions):
        letters[num] = str[index]
      word = "".join(letters).lower()
      if word in words and word not in solutions:
        solutions.append(word)
  elif word == "left":
    for i in range(5):
      if grid[i][0] != grid[i][0].lower():
        letters.append(grid[i][0])
      else:
        letters.append(0)
        count += 1
    for i in range(letters.count(0)):
      positions.append(letters.index(0))
      letters[letters.index(0)] = 1
    randomStr = getRandomStr(grid, count)
    for str in randomStr:
      for index, num in enumerate(positions):
        letters[num] = str[index]
      word = "".join(letters).lower()
      if word in words and word not in solutions:
        solutions.append(word)
  elif word == "middleDown":
    for i in range(5):
      if grid[i][2] != grid[i][2].lower():
        letters.append(grid[i][2])
      else:
        letters.append(0)
        count += 1
    for i in range(letters.count(0)):
      positions.append(letters.index(0))
      letters[letters.index(0)] = 1
    randomStr = getRandomStr(grid, count)
    for str in randomStr:
      for index, num in enumerate(positions):
        letters[num] = str[index]
      word = "".join(letters).lower()
      if word in words and word not in solutions:
        solutions.append(word)
  elif word == "right":
    for i in range(5):
      if grid[i][4] != grid[i][4].lower():
        letters.append(grid[i][4])
      else:
        letters.append(0)
        count += 1
    for i in range(letters.count(0)):
      positions.append(letters.index(0))
      letters[letters.index(0)] = 1
    randomStr = getRandomStr(grid, count)
    for str in randomStr:
      for index, num in enumerate(positions):
        letters[num] = str[index]
      word = "".join(letters).lower()
      if word in words and word not in solutions:
        solutions.append(word)
  return solutions

def solveWaffle(grid):
  solutions = []
  printGrid(grid)
  topWords = solveWord(grid, "top")
  for topWord in topWords:
    grid1 = copy.deepcopy(grid)
    for i in range(5):
      if grid[0][i] == grid[0][i].lower():
        swapLetters(grid, 0, i, topWord[i])
        grid[0][i] = grid[0][i].upper()
    
    middleDownWords = solveWord(grid, "middleDown")
    for middleDownWord in middleDownWords:
      grid2 = copy.deepcopy(grid)
      for i in range(5):
        if grid[i][2] == grid[i][2].lower():
          swapLetters(grid, i, 2, middleDownWord[i])
          grid[i][2] = grid[i][2].upper()
        
      bottomWords = solveWord(grid, "bottom")
      for bottomWord in bottomWords:
        grid3 = copy.deepcopy(grid)
        for i in range(5):
          if grid[4][i] == grid[4][i].lower():
            swapLetters(grid, 4, i, bottomWord[i])
            grid[4][i] = grid[4][i].upper()

        leftWords = solveWord(grid, "left")
        for leftWord in leftWords:
          grid4 = copy.deepcopy(grid)
          for i in range(5):
            if grid[i][0] == grid[i][0].lower():
              swapLetters(grid, i, 0, leftWord[i])
              grid[i][0] = grid[i][0].upper()

          middleAcrossWords = solveWord(grid, "middleAcross")
          for middleAcrossWord in middleAcrossWords:
            grid5 = copy.deepcopy(grid)
            for i in range(5):
              if grid[2][i] == grid[2][i].lower():
                swapLetters(grid, 2, i, middleAcrossWord[i])
                grid[2][i] = grid[2][i].upper()

            rightWords = solveWord(grid, "right")
            for rightWord in rightWords:
              grid6 = copy.deepcopy(grid)
              for i in range(5):
                if grid[i][4] == grid[i][4].lower():
                  swapLetters(grid, i, 4, rightWord[i])
                  grid[i][4] = grid[i][4].upper()
              solutions.append(grid)

              grid = grid6
            grid = grid5
          grid = grid4
        grid = grid3
      grid = grid2
    grid = grid1
  return solutions


def solvePuzzle(grid):
  solutions = solveWaffle(grid)
  
  print(f"{len(solutions)} solutions found: ")

  for grid in solutions:
    printGrid(grid)


grid = [
  ["S", "y", "u", "r", "P"],
  ["a", " ", "i", " ", "n"],
  ["e", "e", "L", "k", "u"],
  ["U", " ", "y", " ", "E"],
  ["P", "m", "a", "r", "E"]
    ]


solvePuzzle(grid)















