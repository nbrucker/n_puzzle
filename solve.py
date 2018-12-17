import heuristic
import error

class Node:
	def __init__(self, puzzle, parent, goal):
		new = []
		for key in puzzle:
			new.append(key[:])
		self.puzzle = new
		self.h = heuristic.getHeuristic(puzzle, goal)
		if (parent):
			self.g = parent.g + 1
		else:
			self.g = 0
		self.f = self.h + self.g
		self.parent = parent
		self.stringify = getStringify(puzzle)

def getStringify(puzzle):
	s = ''
	for key in puzzle:
		for c in key:
			s += str(c) + ','
	return s[:-1]

def swap(puzzle, pos1, pos2):
	tmp = puzzle[pos1[0]][pos1[1]]
	puzzle[pos1[0]][pos1[1]] = puzzle[pos2[0]][pos2[1]]
	puzzle[pos2[0]][pos2[1]] = tmp
	return puzzle

def getChild(parent, positions, direction, goal):
	new = []
	for key in parent.puzzle:
		new.append(key[:])
	if (direction == 'up'):
		new = swap(new, positions, [positions[0] - 1, positions[1]])
	elif (direction == 'down'):
		new = swap(new, positions, [positions[0] + 1, positions[1]])
	elif (direction == 'left'):
		new = swap(new, positions, [positions[0], positions[1] - 1])
	elif (direction == 'right'):
		new = swap(new, positions, [positions[0], positions[1] + 1])
	else:
		error.error('Unexpected error')
	child = Node(new, parent, goal)
	return child

def getChilds(parent, goal):
	childs = []
	positions = heuristic.getPositions(0, parent.puzzle)
	if (positions[0] != 0):
		childs.append(getChild(parent, positions, 'up', goal))
	if (positions[0] != len(parent.puzzle) - 1):
		childs.append(getChild(parent, positions, 'down', goal))
	if (positions[1] != len(parent.puzzle) - 1):
		childs.append(getChild(parent, positions, 'right', goal))
	if (positions[1] != 0):
		childs.append(getChild(parent, positions, 'left', goal))
	return childs

def checkPuzzleExist(state, tab):
	if (state.stringify in tab):
		return tab[state.stringify]
	return None

def getLowest(queue):
	x = -1
	for key in queue:
		if ((key < x or x == -1) and len(queue[key]) > 0):
			x = key
	for key in queue[x]:
		return queue[x][key]
	error.error('Unexpected error')

def solve(puzzle, goal):
	countOpen = 0;
	node = Node(puzzle, None, goal)
	opened = {}
	closed = {}
	queue = {}
	opened[node.stringify] = node
	countOpen += 1;
	queue[node.f] = {}
	queue[node.f][node.stringify] = node
	success = False
	while (len(opened) > 0 and not success):
		state = getLowest(queue)
		if (state.h == 0):
			success = True
		else:
			del opened[state.stringify]
			del queue[state.f][state.stringify]
			closed[state.stringify] = state
			childs = getChilds(state, goal)
			for child in childs:
				inOpen = checkPuzzleExist(child, opened)
				inClose = checkPuzzleExist(child, closed)
				if (inOpen is not None):
					if (child.f < inOpen.f):
						del opened[inOpen.stringify]
						del queue[inOpen.f][inOpen.stringify]
						opened[child.stringify] = child
						if (child.f not in queue):
							queue[child.f] = {}
						queue[child.f][child.stringify] = child
				elif (inClose is not None):
					if (child.f < inClose.f):
						del closed[inClose.stringify]
						opened[child.stringify] = child
						if (child.f not in queue):
							queue[child.f] = {}
						queue[child.f][child.stringify] = child
				else:
					opened[child.stringify] = child
					countOpen += 1;
					if (child.f not in queue):
						queue[child.f] = {}
					queue[child.f][child.stringify] = child

	if (success is False):
		error.error('Unexpected error')
	countState = len(opened) + len(closed)
	moves = state.g
	path = []
	while (state):
		display = ''
		for key in state.puzzle:
			line = ''
			for x in key:
				line += str(x) + ' '
			display += line + '\n'
		path.append(display)
		state = state.parent
	print('Total number of states ever selected in the opened set: ' + str(countOpen))
	print('Maximum number of states: ' + str(countState))
	print('Number of moves: ' + str(moves) + '\n')
	while (moves >= 0):
		print(path[moves])
		moves -= 1
