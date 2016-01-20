import numpy as np
import math

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d

from scipy.interpolate import interp1d

### generate some random (x, y, z) coordinates' matrices
np.random.seed(1) # random seed for consistency

mu_vec1 = np.array([0,0,0])
cov_mat1 = np.array([[100,0,0],[0,100,0],[0,0,100]])
class1_sample = np.random.multivariate_normal(mu_vec1, cov_mat1, 22).T
assert class1_sample.shape == (3,22), "The matrix does not have the required dimension"

mu_vec2 = np.array([0,0,0])
cov_mat2 = np.array([[100,0,0],[0,100,0],[0,0,100]])
class2_sample = np.random.multivariate_normal(mu_vec2, cov_mat2, 22).T
assert class2_sample.shape == (3,22), "The matrix does not have the required dimension"

print class1_sample
print len(class1_sample[0])

### Initialize figure for mapping
fig = plt.figure(figsize=(8,8))


### create an array of the angles
def coord_to_angles(arr):
	angles = []
	for i in range(0, len(arr[0])):
		x = arr[0][i]
		y = arr[1][i]
		temp_angle = math.atan(y/x)

		angles.append(temp_angle)

		print temp_angle
	return angles

coord_to_angles(class1_sample)

### map the angles across time without interpolation
def visualize_angle(arr):
	print "the difference between m1 and m2"
	
	fig = plt.figure(figsize=(8,8))
	ax = fig.add_subplot(111)
	plt.rcParams['legend.fontsize'] = 10
	
	## plot the data
	ax.plot(arr, 'o', markersize=8, color='blue', alpha=0.5)

	plt.title('The difference between the two matrices')
	ax.legend(loc='upper right')

	plt.show()

#visualize_angle(coord_to_angles(class1_sample))

### map the angles across time with interpolation
def visualize_interpolated(arr):
	y = arr
	x = range(0, len(arr))

	
	ax = fig.add_subplot(111)

	f = interp1d(x, y)
	f2 = interp1d(x, y, kind='cubic')

	xnew = np.linspace(min(x), max(x), 100)
	ax.plot(x, y, 'o', xnew, f(xnew), xnew, f2(xnew))

	plt.show()

#visualize_interpolated(coord_to_angles(class1_sample))
visualize_interpolated(coord_to_angles(class2_sample))


### divide the frames up into p
def choose_p(dict, p):
	groups = []
	counter = 0
	for i, j in dict:
		group = []
		group.append(j)
		counter += 1
		if counter == p:
			counter = 0
	return groups

### estimate the score of the fit using the formula
def score(dict, arr, p):
	results = []
	for group in arr:
		summation = 0;
		for el in group:
			summation += mean(dict[el]):
		summation = summation / len(group)
		results.append(summation)

	### Need to edit the score to be more representative and accurate
	return var(results)

### find the offset TODO
########################

### find the mean 
def mean(arr):
	return np.mean(arr);

### find the variance
def variance(arr):
	return np.var(arr);