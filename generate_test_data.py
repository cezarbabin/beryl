import numpy as np
from sklearn.neighbors import NearestNeighbors

## VARIABLES FOR TESTING ##
ROWS = 9
COLUMNS = 90 

## TEST DATA ##
###############
def generate_test_data():
	class1_sample = np.random.rand(ROWS, COLUMNS)
	assert class1_sample.shape == (ROWS, COLUMNS), "The matrix does not have the required dimension"

	output = [[0 for x in range(COLUMNS)] for x in range(ROWS)] 

	for i in range(0, ROWS):
		for j in range(0, COLUMNS):
			var = class1_sample[i][j] * 10
			output[i][j] = (var + 1, var - 1, var + 2)

	print output[1][1]
	print len(output[1])

#joint_vectors = [[0 for x in range(0, COLUMNS*2)] for x in range(ROWS)]

def find_nearest_neighbors(arr):
	nbrs = NearestNeighbors(n_neighbors=2, algorithm='ball_tree').fit(output[1])
	distances, indices = nbrs.kneighbors(output[1])

	print indices                                         
