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
	while (i < len(content)):
		tab = content[i].split(' ')
		if (len(tab) != size):
			error.error('Given size don\'t match puzzle size')
		for x in tab:
			if (isInt(x) == False):
				error.error('Unvalid size')
		puzzle.append(tab)
		i += 1
	return puzzle

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
	print(puzzle)

if __name__ == "__main__":
	main()
