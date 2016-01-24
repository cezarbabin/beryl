
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d

import numpy as np

np.random.seed(1) # random seed for consistency

mu_vec1 = np.array([0,0,0])
cov_mat1 = np.array([[1,0,0],[0,1,0],[0,0,1]])
class1_sample = np.random.multivariate_normal(mu_vec1, cov_mat1, 20).T
assert class1_sample.shape == (3,20), "The matrix does not have the required dimension"

mu_vec2 = np.array([1,1,1])
cov_mat2 = np.array([[1,0,0],[0,1,0],[0,0,1]])
class2_sample = np.random.multivariate_normal(mu_vec2, cov_mat2, 20).T
assert class1_sample.shape == (3,20), "The matrix does not have the required dimension"

def visualize_difference(mat1, mat2):
	print "the difference between m1 and m2"
	
	fig = plt.figure(figsize=(8,8))
	ax = fig.add_subplot(111, projection='3d')
	plt.rcParams['legend.fontsize'] = 10
	
	## plot the data
	ax.plot(class1_sample[0,:], class1_sample[1,:], class1_sample[2,:],
	        'o', markersize=8, color='blue', alpha=0.5, label='class1')
	ax.plot(class2_sample[0,:], class2_sample[1,:], class2_sample[2,:],
	        '^', markersize=8, alpha=0.5, color='red', label='class2')

	plt.title('The difference between the two matrices')
	ax.legend(loc='upper right')

	plt.show()

def compute_mean_vector(mat):
	print "the vector"

def compute_scatter_matrix(mat):
	print "scatter matrix"

def eigen(mat):
	print "eigenvector is ... eigenvalue is ..."

def pca(mat):
	print "embedded PCA"

if __name__ == "__main__":
	a = 1
	b = 2
	visualize_difference(a, b)


#### Benchmark using nearpy and estimate performance 
