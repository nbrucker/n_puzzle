import error

manhattanPosition = {}

def getPositions(number, puzzle):
	i = 0
	length = len(puzzle)
	while (i < length):
		j = 0
		while (j < length):
			if (puzzle[i][j] == number):
				return i, j
			j += 1
		i += 1
	error.error('Unexpected error')

def getManhattan(puzzle, goal):
	global manhattanPosition
	h = 0
	i = 0
	length = len(puzzle)
	while (i < length):
		j = 0
		while (j < length):
			if (puzzle[i][j] != 0 and puzzle[i][j] != goal[i][j]):
				if (puzzle[i][j] in manhattanPosition):
					positions = manhattanPosition[puzzle[i][j]]
				else:
					positions = getPositions(puzzle[i][j], goal)
					manhattanPosition[puzzle[i][j]] = positions
				h += abs(i - positions[0]) + abs(j - positions[1])
			j += 1
		i += 1
	return h

def getHeuristic(puzzle, goal):
	return getManhattan(puzzle, goal)
