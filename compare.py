
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d

import numpy as np
import sys
import plot
import parse
import math

scatter_matrix = []
cov_matrix = []
mean_vector = []

FT_JOINT_LIST = ["RightForeArm", "RightArm", "RightHand", "RightShoulder",
				"LeftForeArm", "LeftArm", "LeftHand", "LeftShoulder", "Head"]

SESSION_11 = [(1371, 1503), (1788, 2037), (2425, 2540), (3000, 3116), (4191, 4295), 
			(4795, 5049), (5471, 5728), (6172, 6342), (6807, 6963), (7602, 7770)]


np.random.seed(1) # random seed for consistency


## TEST DATA ##
mu_vec1 = np.array([0,0,0])
cov_mat1 = np.array([[1,0,0],[0,1,0],[0,0,1]])
class1_sample = np.random.multivariate_normal(mu_vec1, cov_mat1, 20).T
assert class1_sample.shape == (3,20), "The matrix does not have the required dimension"

mu_vec2 = np.array([1,1,1])
cov_mat2 = np.array([[1,0,0],[0,1,0],[0,0,1]])
class2_sample = np.random.multivariate_normal(mu_vec2, cov_mat2, 20).T
assert class2_sample.shape == (3,20), "The matrix does not have the required dimension"

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
	eig_val_cov, eig_vec_cov = np.linalg.eig(cov_matrix)

	for i in range(len(eig_val_sc)):
	    eigvec_sc = eig_vec_sc[:,i].reshape(1,3).T
	    eigvec_cov = eig_vec_cov[:,i].reshape(1,3).T

def pca(mat):
	print "embedded PCA"

def main(a, joints_array):
	shot_nr_1 = (1371, 3216)
	length = shot_nr_1[1] - shot_nr_1[0]

	plot_rms_arrays = []
	plot_arr = []

	for joint in joints_array:
		rms_arr = []
		for i in range(shot_nr_1[0], shot_nr_1[1]):
			x = a[i][joint][0]
			y = a[i][joint][1]
			z = a[i][joint][2]
			rms = math.sqrt(float(1)/3 *( x**2 + y**2 + z**2))
			rms_arr.append(rms)
		plot_rms_arrays.append(rms_arr)

	for array in plot_rms_arrays :
		plot_arr.append(([i for i in range(length)], array))

	plot.draw(plot_arr)


if __name__ == "__main__":
	arr2 = parse.motion_data('motion_files/fahim_11_Char00', "")
	main(arr2, ["RightForeArm", "RightArm", "RightHand"])
	
	#visualize_difference(a, b)


#### Benchmark using nearpy and estimate performance 
