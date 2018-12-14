import time

import heuristic
import error

timeHeuristic = 0

class Node:
	def __init__(self, puzzle, parent, goal):
		new = []
		for key in puzzle:
			x = []
			for c in key:
				x.append(c)
			new.append(x)
		self.puzzle = new
		global timeHeuristic
		start_time = time.clock()
		self.h = heuristic.getHeuristic(puzzle, goal)
		timeHeuristic += time.clock() - start_time
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
		x = []
		for c in key:
			x.append(c)
		new.append(x)
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
	timeFind = 0
	timeChilds = 0
	timeInsert = 0
	timeLowest = 0
	node = Node(puzzle, None, goal)
	opened = {}
	closed = {}
	queue = {}
	opened[node.stringify] = node
	queue[node.f] = {}
	queue[node.f][node.stringify] = node
	success = False
	while (len(opened) > 0 and not success):
		start_time = time.clock()
		state = getLowest(queue)
		timeLowest += time.clock() - start_time
		if (state.h == 0):
			success = True
		else:
			del opened[state.stringify]
			del queue[state.f][state.stringify]
			closed[state.stringify] = state
			start_time = time.clock()
			childs = getChilds(state, goal)
			timeChilds += time.clock() - start_time
			for child in childs:
				start_time = time.clock()
				inOpen = checkPuzzleExist(child, opened)
				inClose = checkPuzzleExist(child, closed)
				timeFind += time.clock() - start_time
				if (inOpen is not None):
					if (child.f < inOpen.f):
						del opened[inOpen.stringify]
						del queue[inOpen.f][inOpen.stringify]
						start_time = time.clock()
						opened[child.stringify] = child
						if (child.f not in queue):
							queue[child.f] = {}
						queue[child.f][child.stringify] = child
						timeInsert += time.clock() - start_time
				elif (inClose is not None):
					if (child.f < inClose.f):
						del closed[inClose.stringify]
						start_time = time.clock()
						opened[child.stringify] = child
						if (child.f not in queue):
							queue[child.f] = {}
						queue[child.f][child.stringify] = child
						timeInsert += time.clock() - start_time
				else:
					start_time = time.clock()
					opened[child.stringify] = child
					if (child.f not in queue):
						queue[child.f] = {}
					queue[child.f][child.stringify] = child
					timeInsert += time.clock() - start_time

	if (success is False):
		error.error('Unexpected error')
	print('find: ' + str(timeFind))
	print('childs: ' + str(timeChilds))
	print('insert: ' + str(timeInsert))
	print('lowest: ' + str(timeLowest))
	global timeHeuristic
	print('heuristic: ' + str(timeHeuristic))
	print(state.puzzle)
