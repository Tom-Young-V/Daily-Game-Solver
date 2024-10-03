import re

txt = open("deluxeGridsData.txt", encoding="UTF-8").read()
lines = txt.split("\n")

allGrids = []

for x, line in enumerate(lines):
	allGrids.append(eval(line))

with open("allDeluxeGrids.py", "w") as file:
    file.write("deluxeGrids = " + repr(allGrids))