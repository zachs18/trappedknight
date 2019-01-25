from typing import Optional, List, Tuple, Callable, Generator

Coordinate = Tuple[int, int]
Move = Tuple[int, int]

def coord_to_number_full(x: int, y: int) -> int:
	"""
	(0,0) -> 1
	Square spirals around
	"""
	if x == y == 0:
		return 1
	elif x == -y and x > 0:
		# full square
		side = 2*x+1
		return side*side
	elif x > 0 and -x < y <= x: # Left part (excl bottom corner)
		# inner square: (2*x-1)**2
		# how far up from bottom corner: (x+y)
		# total: (2*x-1)**2 + (x+y)
		inner_side = 2*x-1
		return inner_side*inner_side + x + y
	elif y > 0 and -y < -x <= y: # Top part (ELC)
		# inner square: (2*y-1)**2
		# full left side (EBC): 2*y
		# top side: (y-x)
		# total: (2*y-1)**2 + 2*y + (y-x)
		inner_side = 2*y-1
		return inner_side*inner_side + 3*y - x
	elif x < 0 and x < -y <= -x: # Right part (ETC)
		# inner square: (2*x+1)**2 # x < 0 remember
		# full left side (EBC): 2*(-x)
		# full top side (ELC): 2*(-x)
		# right side: -(x + y)
		# total: (2*x+1)**2 + 4*(-x) + (-x+-y)
		n_inner_side = 2*x+1 # negative
		return n_inner_side*n_inner_side -(5*x+y)
	else: #if y < 0 and y < x <= -y # Bottom part (ERC)
		# inner square: (2*y+1)**2 # y < 0 remember
		# full left side (EBC): 2*(-y)
		# full top side (ELC): 2*(-y)
		# full right side (ETC): 2*(-y)
		# bottom side: (x-y)
		# total: (2*y+1)**2 + 6*(-y) + (x-y)
		n_inner_side = 2*y+1 # negative
		return n_inner_side*n_inner_side + x - 7*y

def Tr(x: int) -> int:
	return (x*(x+1))//2

def coord_to_number_quadrant_diagonal(x: int, y: int) -> int:
	"""
	1-2 4 7  11  ...
	 / / /  /
	3 5 8  12  ...
	 / /  /
	6 9  13  ...
	 /  /
	10 14  ...
	  /
	15  ...
	...
	"""
	x, y = abs(x), abs(y) # Usable for any quadrant
	if not x:
		return Tr(y+1)
	else:
		return Tr(x+y+1)-x

def knight_path(startx: int = 0, starty: int = 0,
                   xmin: Optional[int] = None, ymin: Optional[int] = None,
                   xmax: Optional[int] = None, ymax: Optional[int] = None,
                   number_func: Callable[[int, int], int] = None,
                   moves: List[Move] = [(1,2),(2,1),(-1,2),(-2,1),(1,-2),(2,-1),(-1,-2),(-2,-1)]
) -> Generator[Tuple[int, Coordinate, int], None, Tuple[List[Coordinate]]]:
	if xmin is None:
		if xmax is None:
			xcheck = None
		else:
			xcheck = lambda x: x <= xmax
	else:
		if xmax is None:
			xcheck = lambda x: xmin <= x
		else:
			xcheck = lambda x: xmin <= x <= xmax
	if ymin is None:
		if ymax is None:
			ycheck = None
		else:
			ycheck = lambda y: y <= ymax
	else:
		if ymax is None:
			ycheck = lambda y: ymin <= y
		else:
			ycheck = lambda y: ymin <= y <= ymax

	if number_func == None:
		if {xmin, xmax, ymin, ymax} == {None}: # Traditional problem
			number_func = coord_to_number_full
		elif {xmin, xmax} == {0, None} == {ymin, ymax}: # Corner
			number_func = coord_to_number_quadrant_diagonal
		elif {xmin, xmax} == {0, None} and {ymin, ymax} == {None}: # Left or right half
			number_func = coord_to_number_half_horizontal
		elif {ymin, ymax} == {0, None} and {xmin, xmax} == {None}: # Top or bottom half
			number_func = coord_to_number_half_vertical
		else:
			raise ValueError("Could not deduce default number_func for boundary %r<=x<=%r, %r<=y<=%r" % (xmin, xmax, ymin, ymax))
	x, y = startx, starty
	used: List[Coordinate] = [(x, y)]
	usednumbers: List[int] = [number_func(x, y)]
	yield (len(used), (x, y), number_func(x, y))
	while True:
		bestmove = -1
		bestnumber = float('inf')
		for move, (dx, dy) in enumerate(moves):
			nx, ny = x+dx, y+dy
			if (xcheck is None or xcheck(nx)) and (ycheck is None or ycheck(ny)) and (nx, ny) not in used:
				number = number_func(nx, ny)
				if number < bestnumber:
					bestmove = move
					bestnumber = number
		if bestmove < 0:
			return (used, (startx, starty), (x, y))
		x += moves[bestmove][0]
		y += moves[bestmove][1]
		used.append((x, y))
		usednumbers.append(bestnumber)
		yield (len(used), (x, y), bestnumber)

def knight_path_stats(stats: List, *args, **kwargs):
	_stats = yield from knight_path(*args, **kwargs)
	stats.append(_stats)

if __name__ == "__main__":
	stats = []
	for i, (nx, ny), num in knight_path_stats(stats, xmin=0, ymin=0):
		print(i, (nx, ny), num)
	print(stats)
