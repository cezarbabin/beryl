
#from matplotlib import pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D
#from mpl_toolkits.mplot3d import proj3d

import numpy as np
import sys
#import plot
import parse
import math

scatter_matrix = []
cov_matrix = []
mean_vector = []

FT_JOINT_LIST = ["RightForeArm", "RightArm", "RightHand", "RightShoulder",
				"LeftForeArm", "LeftArm", "LeftHand", "LeftShoulder", "Head"]

SESSION_02 = [(2065, 2235), (2627. 2745), (3472, 3606), (4142, 4288), (4854, 4976), 
      (7644, 7768), (8388, 8513), (9024, 9152), (9523, 9656), (10485, 10644)]

SESSION_03 = [(1793 ,1905), (2428, 2578), (3244, 3368), (4082, 4213), (4881, 5022), 
      (5557, 5726), (6265, 6427), (6919, 7054), (7677, 7796), (8443, 8567)]

SESSION_04 = [(2144, 2272), (3083, 3198), (3829, 3952), (4919, 5076), (5559, 5684),
      (6261, 6383), (9147, 9278), (9941, 10061), (10539, 10660), (11230, 11341)]

SESSION_05 = [(1571, 1695), (2072, 2201), (2681, 2807), (3791, 3899), (4731, 4839),
      (5241, 5352), (6009, 6119), (7068, 7180), (7794, 7916), (8315, 8430)]

SESSION_06 = [(1194, 1306), (1707, 1815), (2357. 2469), (2929, 3081), (3529. 3659),
      (4274, 4402), (4969, 5094), (5785, 5921), (6561, 6673), (7135, 7281)]

SESSION_07 = [(1493, 1624), (2126, 2242), (2826, 2958), (3335, 3477), (4413, 4557),
      (5765, 5911), (6937, 7059), (7488, 7611), (9279, 9426), (9969, 10114)]

SESSION_08 = [(1585, 1706), (2211, 2340), (3032, 3173), (3611, 3723), (4347, 4481),
      (5056, 5186), (5762, 5901), (6221, 6345), (7052, 7165), (7897, 8025)]

SESSION_09 = [(1455, 1577), (2193, 2332), (3615, 3747), (4261, 4399), (5053, 5180),
      (5663, 5800), (6232, 6362), (7088, 7222), (8242, 8384), (8819, 8940)]

SESSION_10 = [(1591, 1704), (2286, 2416), (3182, 3317), (3762, 3914), (4439, 4575),
      (5101, 5236), (7120, 7246), (7709, 7845), (8464, 8586), (9127, 9253)]

SESSION_11 = [(1371, 1503), (1788, 2037), (2425, 2540), (3000, 3116), (4191, 4295), 
			(4795, 5049), (5471, 5728), (6172, 6342), (6807, 6963), (7602, 7770)]

SESSION_13 = [(1527,1652),(2175,2291),(2842,2969),(3640,3769),(4300,4425),(5328,5443),
			(6290,6410),(6975,7091),(7740,7862),(8792,8907)]

SESSION_14 = [(1287, 1415), (2302, 2434), (3213, 3360), (4061, 4183), (4719, 4842),
      (5300, 5419), (5971, 6115), (6655, 6782), (7699, 7822), (8488, 8619)]

SESSION_15 = [(2351, 2482), (3232, 3397), (4146,  4296), (5501, 5640), (6129, 6261), 
			(6712, 6858), (7340, 7491), (8364, 8469), (9150, 9284), (10224, 10343)]

SESSION_16 = [(1483, 1618), (3159, 3295), (3914, 4049), (4699, 4817), (5302, 5444),
      (5927, 6094), (6923, 7075), (7664, 7796), (8265, 8426), (9265, 9432)]

SESSION_17 = [(1360, 1537), (2067, 2258), (2860, 3002), (3418, 3571), (4066, 4217),
      (4815, 4975), (5514, 5683), (6177, 6342), (7105, 7247), (7814, 7954)]

SESSION_19 = [(1511, 1666), (2213, 2372), (2791, 2916), (3372, 3525), (4162, 4332),
      (4831, 4971), (5461, 5595), (6316, 6477), (6962, 7098), (7610, 7737)]

SESSION_20 = [(1840, 1992), (2873, 3003), (3631, 3776), (4362, 4487), (5005, 5135),
      (5629, 5783), (6398, 6544), (7141, 7272), (8111, 8246), (8646, 8774)]


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

# def visualize_difference(mat1, mat2):
# 	print "the difference between m1 and m2"

# 	fig = plt.figure(figsize=(8,8))
# 	ax = fig.add_subplot(111, projection='3d')
# 	plt.rcParams['legend.fontsize'] = 10
	
# 	## plot the data
# 	ax.plot(class1_sample[0,:], class1_sample[1,:], class1_sample[2,:],
# 	        'o', markersize=8, color='blue', alpha=0.5, label='class1')
# 	ax.plot(class2_sample[0,:], class2_sample[1,:], class2_sample[2,:],
# 	        '^', markersize=8, alpha=0.5, color='red', label='class2')

# 	plt.title('The difference between the two matrices')

# 	ax.legend(loc='upper right')

# 	plt.show()

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

def main(a, joints_array, i, session):
	shot_nr_1 = session[i]
	length = shot_nr_1[1] - shot_nr_1[0]

	plot_rms_arrays = []
	position_arrays = []
	
	for joint in joints_array:
		rms_arr = []
		position_arr = []
		for i in range(shot_nr_1[0], shot_nr_1[1]):
			x = a[i][joint][0]
			y = a[i][joint][1]
			z = a[i][joint][2]
			rms = math.sqrt(float(1)/3 *( x**2 + y**2 + z**2))
			rms_arr.append(rms)
			position_arr.append((x,y,z))
		plot_rms_arrays.append(rms_arr)
		position_arrays.append(position_arr)
	return plot_rms_arrays, position_arrays

def plot_data(plot_rms_arrays):
	plot_arr = []
	for array in plot_rms_arrays :
		plot_arr.append(([i for i in range(len(plot_rms_arrays[0]))], array))
	plot.draw(plot_arr)

if __name__ == "__main__":
	arr2 = parse.motion_data('motion_files/fahim_11_Char00', "")
	filtered_arrays = compare.main(arr2, ["RightForeArm", "RightArm", "RightHand"])
	plot_data(filtered_arrays)

	
	#visualize_difference(a, b)


#### Benchmark using nearpy and estimate performance 
