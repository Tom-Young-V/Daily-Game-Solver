from waffleSolver import WaffleSolver
import sys
sys.path.append('./Waffle Web Scraping')
from allGrids import dailyGrids, deluxeGrids
import time

def testSolver(grids, size, amountSwaps):
	startTime = time.time()
	failedGrids = []
	for x, grid in enumerate(grids):
		if size == "daily" and not (x + 1) % 100 or size == "deluxe" and not (x + 1) % 10:
			print(f"Reached grid {x + 1} / {len(grids)}")

		solver = WaffleSolver(grid, size)
		solver.solve(False, amountSwaps)

		if solver.failed:
			failedGrids.append(x)
			print(f"Failed grid {x + 1}, {solver.failed}")

	totalTime = time.time() - startTime
	print()
	print(f"Took {round(totalTime, 3)} seconds to solve {len(grids)} Waffles")
	print(f"Average solve time: {round(totalTime / len(grids), 3)} seconds")
	print(f"Solved {len(grids) - len(failedGrids)} / {len(grids)}")
	print(f"Solve rate: {round(100 * (len(grids) - len(failedGrids)) / len(grids), 3)} %")
	print(f"Failed grids: {failedGrids}")

testSolver(dailyGrids, "daily", 15)
testSolver(deluxeGrids, "deluxe", 25)











# Failed grids for daily
if False:
	failedGrids = [11, 37, 63, 73, 80, 82, 83, 84, 86, 92, 106, 118, 121, 133, 395]  # add 1 for actual name

	for x in failedGrids:
		print(x + 1)
		failedGrid = dailyGrids[x]

		solver = WaffleSolver(failedGrid, "daily")
		solver.solve(True)

# Current daily fails: 12, 38, 64, 74, 81, 83, 84, 85, 87, 93, 107, 119, 122, 134, 396 - (Subtract 1 for index in allGrids list)
# All of them create 2 solutions with very similar results (ie: adobe instead of abode)


# testSolver(deluxeGrids, "deluxe", 25)

# Current deluxe fails: 27, 41, 43, 72, 83
# 27, 41, 43, 72, 83 find multiple solutions


if True:
	failedDeluxeGrids = [26, 40, 42, 71, 82]

	for x in failedDeluxeGrids:
		print(x + 1)
		failedGrid = deluxeGrids[x]

		solver = WaffleSolver(failedGrid, "deluxe")
		solver.solve(True, 25)








