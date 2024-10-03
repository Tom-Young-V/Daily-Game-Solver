from collections import defaultdict
from lastGrid import lastGrid

words = open("allwords.txt", encoding="UTF-8").read()
words = words.split("\n")


words = [word.strip() for word in words if word]

wordsToAdd = []
wordsToRemove = []

for word in wordsToAdd:
    if word in words:
        print("FAILED", word)
    else:
        words.append(word)

for word in wordsToRemove:
    if word in words:
        words.remove(word)
    else:
        print("FAILED", word)


words.sort()


# Write the sorted words back to the file
with open('allwords.txt', 'w') as file:
    for word in words:
        file.write(word + '\n')


with open("allwords.py", "w") as file:
    file.write(f"allwords = {repr(words)}\n")

with open("lastGrid.py", "w") as file:
    file.write(f"lastGrid = ((), ())")


# allwords = defaultdict(list)

# for word in words:
#     if not word:
#         continue

#     allwords[word[0]].append(word)

# with open("wordslistdict.py", "w") as file:
#     file.write(f"wordslistdict = {dict(allwords)}\n")
