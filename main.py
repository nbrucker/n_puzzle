import sys

import error

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
	size = content[0]
	if (isInt(size) == False):
		error.error('Unvalid size')
	size = int(size)
	i = 1
	puzzle = []
	values = []
	while (i < len(content)):
		tab = content[i].split(' ')
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
	return puzzle

# def getSnail(puzzle):
# 	tab = []
# 	puzzle_len = len(puzzle)
# 	i = 0
# 	j = 0
# 	while (len(tab) != puzzle_len * puzzle_len):
# 		while (j < puzzle_len and puzzle[i][j] not in tab):
# 			tab.append(puzzle[i][j])
# 			j += 1
# 		j -= 1
# 		i += 1
# 		while (i < puzzle_len and puzzle[i][j] not in tab):
# 			tab.append(puzzle[i][j])
# 			i += 1
# 		i -= 1
# 		j -= 1
# 		while (j >= 0 and puzzle[i][j] not in tab):
# 			tab.append(puzzle[i][j])
# 			j -= 1
# 		j += 1
# 		i -= 1
# 		while (i >= 0 and puzzle[i][j] not in tab):
# 			tab.append(puzzle[i][j])
# 			i -= 1
# 		i += 1
# 		j += 1
# 	return tab

# def getInversions(puzzle):
# 	puzzle.remove(0)
# 	inversions = 0
# 	i = 0
# 	while (i < len(puzzle)):
# 		j = i + 1
# 		while (j < len(puzzle)):
# 			if (puzzle[j] < puzzle[i]):
# 				inversions += 1
# 			j += 1
# 		i += 1
# 	return inversions

# def getZeroLine(puzzle):
# 	i = len(puzzle) - 1
# 	while (i >= 0):
# 		if (0 in puzzle[i]):
# 			return len(puzzle) - i
# 		i -= 1
# 	error.error('Unexpected error')
#
# def checkSolvable(puzzle):
# 	inversions = getInversions(getSnail(puzzle))
# 	if (len(puzzle) % 2 == 0):
# 		line = getZeroLine(puzzle)
# 		print(line)
# 		print(line % 2)
# 		print(inversions)
# 		print(inversions % 2)
# 		if (line % 2 == 0 and inversions % 2 == 0):
# 			error.error('Puzzle unsolvable')
# 		elif (line % 2 != 0 and inversions % 2 != 0):
# 			error.error('Puzzle unsolvable')
# 	elif (inversions % 2 != 0):
# 			error.error('Puzzle unsolvable')

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
	print(start % 2 == end % 2)


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
	if (len(sys.argv) != 2):
		error.error('python main.py [file]')
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

if __name__ == "__main__":
	main()
