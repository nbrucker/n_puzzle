import copy
import time

import heuristic
import error

class Node:
	def __init__(self, puzzle, parent, goal):
		self.puzzle = copy.deepcopy(puzzle)
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
	new = copy.deepcopy(parent.puzzle)
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
	index = 0
	for key in tab:
		if (state.stringify == key.stringify):
			return index
		index += 1
	return -1

def insertOpen(state, opened):
	index = 0
	for key in opened:
		if (key.f > state.f):
			break
		else:
			index += 1
	opened = opened[:index] + [state] + opened[index:]
	return opened

def solve(puzzle, goal):
	timeFind = 0
	timeChilds = 0
	timeInsert = 0
	node = Node(puzzle, None, goal)
	opened = [node]
	closed = []
	success = False
	while (len(opened) > 0 and not success):
		state = opened[0]
		if (state.h == 0):
			success = True
		else:
			del opened[0]
			closed.append(state)
			start_time = time.clock()
			childs = getChilds(state, goal)
			timeChilds += time.clock() - start_time
			for child in childs:
				start_time = time.clock()
				inOpen = checkPuzzleExist(child, opened)
				inClose = checkPuzzleExist(child, closed)
				timeFind += time.clock() - start_time
				if (inOpen != -1):
					if (child.f < opened[inOpen].f):
						del opened[inOpen]
						start_time = time.clock()
						opened = insertOpen(child, opened)
						timeInsert += time.clock() - start_time
				elif (inClose != -1):
					if (child.f < closed[inClose].f):
						del closed[inClose]
						start_time = time.clock()
						opened = insertOpen(child, opened)
						timeInsert += time.clock() - start_time
				else:
					start_time = time.clock()
					opened = insertOpen(child, opened)
					timeInsert += time.clock() - start_time
	if (success is False):
		error.error('Unexpected error')
	print('find: ' + str(timeFind))
	print('childs: ' + str(timeChilds))
	print('insert: ' + str(timeInsert))
	print(state.puzzle)

