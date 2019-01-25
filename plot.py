import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import signal
import sys

import trappedknight

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

stats = []
#moves = [(i, j) for i in [-3,-2,2,3] for j in [-3,-2,2,3] if abs(i)!=abs(j)]
#path_gen = trappedknight.knight_path(stats, number_func = lambda x,y: x*x+4*y*y)
#path_gen = trappedknight.knight_path(stats,  moves=moves)
#path_gen = trappedknight.knight_path(stats, xmin=0, xmax=100, ymax=0, ymin=-49, number_func=lambda *a: 0)
#path_gen = trappedknight.knight_path(stats, xmin=0, ymax=0)
path_gen = trappedknight.knight_path(stats)
path_gen.send(None)
points = stats[-1][0]
plot_and_continue = False
plot_and_exit = False

def signal_handler(sig, frame):
	global plot_and_continue
	if not plot_and_continue:
		plot_and_continue = True
	else:
		try:
			print("Quitting")
		except RuntimeError:
			sys.exit(45)
		sys.exit()
signal.signal(signal.SIGINT, signal_handler)

while True:
	try:
		arg = path_gen.send(plot_and_continue)
	except StopIteration:
		plot_and_continue = plot_and_exit = True
	if not plot_and_continue:
		continue
	#else plot
	print("\x1b[GPlotting current progress")
	del stats[:-1] # clean up
	print(len(stats[-1][0]))
	points = stats[-1][0]
	minx = min(x for x,y in points)
	miny = min(y for x,y in points)
	maxx = max(x for x,y in points)
	maxy = max(y for x,y in points)
	print(1)
	xticks = np.arange(minx-0.5, maxx+1, 1)
	yticks = np.arange(miny-0.5, maxy+1, 1)
	print(2)

	ax.set_xticks(xticks)
	print(3.5)
	ax.set_yticks(yticks)
	print(3)

	ax.grid(which="both")
	print(4)

	plt.plot(*zip(*points))
	print(5)
	plt.plot(*points[0], "ro")
	plt.plot(*points[-1], "rx")
	plt.savefig("foo.png")
	print(6)

	plt.show()
	plot_and_continue = False
	if plot_and_exit:
		break
