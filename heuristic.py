import sys

import error

goalPosition = {}

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

def getPositionsFromGoal(number, goal):
	if (number in goalPosition):
		positions = goalPosition[number]
	else:
		positions = getPositions(number, goal)
		goalPosition[number] = positions
	return positions

def getManhattan(puzzle, goal):
	global goalPosition
	h = 0
	i = 0
	length = len(puzzle)
	while (i < length):
		j = 0
		while (j < length):
			if (puzzle[i][j] != 0 and puzzle[i][j] != goal[i][j]):
				positions = getPositionsFromGoal(puzzle[i][j], goal)
				h += abs(i - positions[0]) + abs(j - positions[1])
			j += 1
		i += 1
	return h

def getHamming(puzzle, goal):
	global goalPosition
	h = 0
	i = 0
	length = len(puzzle)
	while (i < length):
		j = 0
		while (j < length):
			if (puzzle[i][j] != 0 and puzzle[i][j] != goal[i][j]):
				positions = getPositionsFromGoal(puzzle[i][j], goal)
				if (i != positions[0] or j != positions[1]):
					h += 1
			j += 1
		i += 1
	return h

def isInConflicts(conflicts, a, b):
	s1 = str(a) + ',' + str(b)
	s2 = str(b) + ',' + str(a)
	if (s1 in conflicts or s2 in conflicts):
		return True
	return False

def getLinear(puzzle, goal):
	global goalPosition
	conflicts = {}
	h = 0
	c = 0
	i = 0
	length = len(puzzle)
	while (i < length):
		j = 0
		while (j < length):
			if (puzzle[i][j] != 0 and puzzle[i][j] != goal[i][j]):
				positions = getPositionsFromGoal(puzzle[i][j], goal)
				h += abs(i - positions[0]) + abs(j - positions[1])
				if (i == positions[0] and j != positions[1]):
					x = -1 if (positions[1] < j) else 1
					n = j + x
					while (n != positions[1] + x):
						tile = puzzle[i][n]
						if (tile != 0):
							positionsTest = getPositionsFromGoal(tile, goal)
							if (positionsTest[0] == positions[0]):
								if (x == 1 and positionsTest[1] <= n):
									if (not isInConflicts(conflicts, puzzle[i][j], tile)):
										conflicts[str(puzzle[i][j]) + ',' + str(tile)] = True
										c += 1
								elif (x == -1 and positionsTest[1] >= n):
									if (not isInConflicts(conflicts, puzzle[i][j], tile)):
										conflicts[str(puzzle[i][j]) + ',' + str(tile)] = True
										c += 1
						n += x
				if (i != positions[0] and j == positions[1]):
					x = -1 if (positions[0] < i) else 1
					n = i + x
					while (n != positions[0] + x):
						tile = puzzle[n][j]
						if (tile != 0):
							positionsTest = getPositionsFromGoal(tile, goal)
							if (positionsTest[1] == positions[1]):
								if (x == 1 and positionsTest[0] <= n):
									if (not isInConflicts(conflicts, puzzle[i][j], tile)):
										conflicts[str(puzzle[i][j]) + ',' + str(tile)] = True
										c += 1
								elif (x == -1 and positionsTest[0] >= n):
									if (not isInConflicts(conflicts, puzzle[i][j], tile)):
										conflicts[str(puzzle[i][j]) + ',' + str(tile)] = True
										c += 1
						n += x
			j += 1
		i += 1
	return h + (2 * c)

def getHeuristic(puzzle, goal):
	if (sys.argv[3] == 0):
		return getHamming(puzzle, goal)
	elif (sys.argv[3] == 1):
		return getManhattan(puzzle, goal)
	else:
		return getLinear(puzzle, goal)
