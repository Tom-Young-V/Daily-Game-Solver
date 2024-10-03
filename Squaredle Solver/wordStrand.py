class WordStrand:
	def __init__(self, indexes, currentIndex, word, possibleWords = False):
		self.indexes = indexes
		self.currentIndex = currentIndex
		self.word = word
		self.possibleWords = possibleWords

	def __str__(self):
		return f"{self.word}, {self.indexes}"

	def __repr__(self):
		return f"{self.word}"

	def copy(self):
		return WordStrand(self.indexes.copy(), self.currentIndex, self.word, self.possibleWords)

	def addLetter(self, index, letter):
		self.indexes.append(index)
		self.currentIndex = index
		self.word += letter
		