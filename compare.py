
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d

import numpy as np

scatter_matrix = []
cov_matrix = []
mean_vector = []

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
	mean_x = np.mean(all_samples[0,:])
	mean_y = np.mean(all_samples[1,:])
	mean_z = np.mean(all_samples[2,:])

	mean_vector = np.array([[mean_x],[mean_y],[mean_z]])
	print "the mean vector has been calculated"
	return mean_vector

def compute_scatter_matrix(mat):
	scatter_matrix = np.zeros((3,3))
	for i in range(all_samples.shape[1]):
		el1 = all_samples[:,i].reshape(3,1) - mean_vector
		el2 = all_samples[:,i].reshape(3,1) - mean_vector
    	scatter_matrix += (el1).dot((el2).T)
	print "scatter matrix"
	return scatter_matrix

def covariance_matrix(mat):
	cov_matrix = np.cov([all_samples[0,:],all_samples[1,:],all_samples[2,:]])
	return cov_matrix

def eigen(mat):
	eig_val_sc, eig_vec_sc = np.linalg.eig(scatter_matrix)

	# eigenvectors and eigenvalues for the from the covariance matrix
	eig_val_cov, eig_vec_cov = np.linalg.eig(cov_mattrix)

	for i in range(len(eig_val_sc)):
	    eigvec_sc = eig_vec_sc[:,i].reshape(1,3).T
	    eigvec_cov = eig_vec_cov[:,i].reshape(1,3).T

def pca(mat):
	print "embedded PCA"

if __name__ == "__main__":
	a = 1
	b = 2
	visualize_difference(a, b)


#### Benchmark using nearpy and estimate performance 
