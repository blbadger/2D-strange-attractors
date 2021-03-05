import numpy as np 
from matplotlib import pyplot as plt
plt.style.use('dark_background')
import copy

def henon_map(x, y, a, b):
	x_next = 1 - a*x**2 + y
	y_next = b*x
	return x_next, y_next

def reverse_henon_stability(max_iterations, a, b, x_range, y_range):
	xl, xr = -2, 2
	yl, yr = 1, -1

	x_list = np.arange(xl, xr, (xr - xl)/x_range)
	y_list = np.arange(yl, yr, -(yl - yr)/y_range)
	array = np.meshgrid(x_list[:x_range], y_list[:y_range])

	x2 = np.zeros(x_range)
	y2 = np.zeros(y_range)
	iterations_until_divergence = np.meshgrid(x2, y2)

	for i in iterations_until_divergence:
		for j in i:
			j += max_iterations

	not_already_diverged = np.ones(np.shape(iterations_until_divergence))
	not_already_diverged = not_already_diverged[0] < 1000

	for k in range(max_iterations):
		x_array_copied = copy.deepcopy(array[0]) # copy array to prevent premature modification of x array

		# henon map applied to array 
		array[0] = array[1] / b
		array[1] = a * (array[1] / b)**2 + x_array_copied - 1

		r = (array[0]**2 + array[1]**2)**0.5
		diverging = (r > 100) & not_already_diverged
		not_already_diverged = np.invert(diverging) & not_already_diverged
		iterations_until_divergence[0][diverging] = k

	return iterations_until_divergence[0]

x, y = 1, 1
a, b = 1.4, 0.3
ls = [[x, y]]

steps = 100000
X = [0 for i in range(steps)]
Y = [0 for i in range(steps)]

X[0], Y[0] = 0, 0 # initial point

for i in range(steps-1):
	if abs(X[i] + Y[i])**2 < 1000:
		X[i+1] = henon_map(X[i], Y[i], a, b)[0]
		Y[i+1] = henon_map(X[i], Y[i], a, b)[1]


for t in range(0, 1):
	a = 1.4
	b = 0.3 + 0.0001*t

	steps = 10000
	X = [0 for i in range(steps)]
	Y = [0 for i in range(steps)]

	X[0], Y[0] = 0, 0 # initial point

	for i in range(steps-1):
		if abs(X[i] + Y[i])**2 < 1000:
			X[i+1] = henon_map(X[i], Y[i], a, b)[0]
			Y[i+1] = henon_map(X[i], Y[i], a, b)[1]

	plt.plot(X, Y, ',', color='white', alpha = 0.5, markersize = 0.2)
	plt.imshow(reverse_henon_stability(200, a, b, x_range=2000, y_range=1400), extent=[-2, 2, -1, 1], aspect=2, cmap='inferno', alpha=1)
	plt.axis('off')
	plt.tick_params(labelsize=6)
	plt.show()
	# plt.savefig('henon_reversed_{0:03d}.png'.format(t), dpi=420, bbox_inches='tight', pad_inches=0)
	plt.close()
