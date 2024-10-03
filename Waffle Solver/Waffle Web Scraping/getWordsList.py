words = open("allwords.txt", encoding="UTF-8").read()
words = words.split("\n")

with open("allwords.py", "w") as file:
    file.write("allwords = " + repr(words))
