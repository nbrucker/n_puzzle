import sys
import time

import error
import solve

def cleanContent(content):
	valid = []
	content = content.split('\n')
	for key in content:
		tmp = key.split('#')
		tmp = tmp[0].strip()
		if (len(tmp) > 0 and tmp[0] != '#'):
			valid.append(tmp)
	return valid

def isInt(x):
	try:
		int(x)
		return True
	except:
		return False

def checkContent(content):
	if (len(content) <= 0):
		error.error('Unvalid content')
	size = content[0]
	if (isInt(size) == False):
		error.error('Unvalid size')
	size = int(size)
	i = 1
	puzzle = []
	values = []
	while (i < len(content)):
		tab = content[i].split()
		if (len(tab) != size):
			error.error('Given size don\'t match puzzle size')
		n = 0
		while (n < len(tab)):
			if (isInt(tab[n]) == False):
				error.error('Unvalid size')
			tab[n] = int(tab[n])
			if (tab[n] in values):
				error.error('Same number twice')
			values.append(tab[n])
			n += 1
		puzzle.append(tab)
		i += 1
	i = 0
	while (i < len(values)):
		if (i not in values):
			error.error('Error in puzzle')
		i += 1
	if (len(puzzle) != size):
		error.error('Given size don\'t match puzzle size')
	return puzzle

def getZeroIndex(tab):
	i = 0
	while (i < len(tab)):
		j = 0
		while (j < len(tab[i])):
			if (tab[i][j] == 0):
				return ((i * len(tab)) + j)
			j += 1
		i += 1
	error.error('Unexpected error')

def getInversionsFor(puzzle, i, j, x):
	if (x == 0):
		return 0
	inversions = 0
	while (i < len(puzzle)):
		while (j < len(puzzle[i])):
			if (puzzle[i][j] != 0 and puzzle[i][j] < x):
				inversions += 1
			j += 1
		j = 0
		i += 1
	return inversions

def getInversions(puzzle):
	inversions = 0
	i = 0
	while (i < len(puzzle)):
		j = 0
		while (j < len(puzzle[i])):
			inversions += getInversionsFor(puzzle, i, j, puzzle[i][j])
			j += 1
		i += 1
	return inversions

def checkSolvable(puzzle, goal):
	start = getInversions(puzzle)
	end = getInversions(goal)
	if (len(puzzle) % 2 == 0):
		start += int(getZeroIndex(puzzle) / len(puzzle))
		end += int(getZeroIndex(goal) / len(puzzle))
	if ((start % 2 == end % 2) is False):
		error.error('Unsolvable')

def getGoalState(size):
	goal = []
	for i in range(size):
		tab = []
		for i in range(size):
			tab.append(0)
		goal.append(tab)
	i = 0
	j = 0
	x = 1
	while (x < size * size):
		while (j < size and goal[i][j] == 0 and x < size * size):
			goal[i][j] = x
			x += 1
			j += 1
		j -= 1
		i += 1
		while (i < size and goal[i][j] == 0 and x < size * size):
			goal[i][j] = x
			x += 1
			i += 1
		i -= 1
		j -= 1
		while (j >= 0 and goal[i][j] == 0 and x < size * size):
			goal[i][j] = x
			x += 1
			j -= 1
		j += 1
		i -= 1
		while (i >= 0 and goal[i][j] == 0 and x < size * size):
			goal[i][j] = x
			x += 1
			i -= 1
		i += 1
		j += 1
	return goal

def main():
	if (len(sys.argv) != 4):
		error.error('python main.py [file] -h [0|1|2]')
	if (not isInt(sys.argv[3])):
		error.error('python main.py [file] -h [0|1|2]')
	sys.argv[3] = int(sys.argv[3])
	if (sys.argv[2] != '-h' or sys.argv[3] < 0 or sys.argv[3] > 2):
		error.error('python main.py [file] -h [0|1|2]')
	filename = sys.argv[1]
	content = ''
	try:
		f = open(filename, 'r')
		content = f.read()
		f.close()
	except:
		error.error('error opening file')
	content = cleanContent(content)
	puzzle = checkContent(content)
	goal = getGoalState(len(puzzle))
	checkSolvable(puzzle, goal)
	solve.solve(puzzle, goal)

if __name__ == "__main__":
	start_time = time.clock()
	main()
	print('all: ' + str(time.clock() - start_time))
