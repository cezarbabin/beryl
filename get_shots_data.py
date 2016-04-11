import parse 
import compare
import classifier
from sklearn.neighbors import NearestNeighbors
from sklearn.neighbors import KDTree

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn import neighbors, datasets

motion_arrays = []

SESSION_11 = [(1371, 1503), (1788, 2037), (2425, 2540), (3000, 3116), (4191, 4295), 
			(4795, 5049), (5471, 5728), (6172, 6342), (6807, 6963), (7602, 7770)]

SESSION_15 = [(2351, 2482), (3232, 3397), (4146,  4296), (5501, 5640), (6129, 6261), 
			(6712, 6858), (7340, 7491), (8364, 8469), (9150, 9284), (10224, 10343)]

SESSION_13 = [(1527,1652),(2175,2291),(2842,2969),(3640,3769),(4300,4425),(5328,5443),
			(6290,6410),(6975,7091),(7740,7862),(8792,8907)]

session_array = [0] * 10 + [SESSION_11,0,SESSION_13,0, SESSION_15]


#for i in range(1,21):
for i in range(1,21): 
	if (i == 11 or i == 13 or i == 15):
		string = 'motion_files/fahim_' + str(i) + '_Char00'
		mot_arr = parse.motion_data(string, "")
	else: 
		mot_arr = []
	motion_arrays.append(mot_arr)
	reload(parse)

#
#MOTION_ARRAY11 = parse.motion_data('motion_files/fahim_11_Char00', "")
#reload(parse)
#MOTION_ARRAY13 = parse.motion_data('motion_files/fahim_13_Char00', "")


#MOTION_ARRAY13 = parse.motion_data('motion_files/fahim_13_Char00', "")

def find_nearest_neighbors(arr):
	kdt = KDTree(arr, leaf_size=30, metric='euclidean')
	query = kdt.query(arr, k=2, return_distance=False)

	nbrs = NearestNeighbors(n_neighbors=2, algorithm='ball_tree').fit(arr)
	distances, indices = nbrs.kneighbors(arr)

	return indices 



def main():
	shots = []

	print mot_arr

	for index in range(1, 21):
		for i in range(0,10):
			if (index == 11 or index == 13 or index == 15):
				FILTERED_ARRAYS = compare.main(motion_arrays[index - 1], compare.FT_JOINT_LIST, i, session_array[index - 1])[1]
				shot = classifier.populateA(FILTERED_ARRAYS)
				shots.append(shot)

	#for i in range(0,10):
		#FILTERED_ARRAYS = compare.main(MOTION_ARRAY13, compare.FT_JOINT_LIST, i, compare.SESSION_13)[1]
		#shot = classifier.populateA(FILTERED_ARRAYS)
		#shots.append(shot)

	joint_shots = []
	indices_directory = {}
	print len(shots)

	#for shots in range(0,10):
		#for shot in shots:
			#joint_shots.append(shot[joint])
		#joint_indices = find_nearest_neighbors(joint_shots)
		#indices_directory[joint] = joint_indices
		#joint_shots = []
	joint_indices = find_nearest_neighbors(shots)
	print joint_indices

	seq11 = [5,6,7,9]
	seq13 = [2,4,5,10]
	seq15 = [4,5,6,7,8,9,10]

	for i in range(0, len(seq13)):
		seq13[i] += 10

	for i in range(0, len(seq15)):
		seq15[i] += 20

	seq13 = seq13 + seq11 + seq15


	true = 0
	total = 0

	#for i in range(0,9):
	for j in joint_indices:
		total +=1
		if(j[0] + 1 in seq13 and j[1] + 1 in seq13):
			true += 1
		if((not (j[0] + 1 in seq13)) and (not(j[1] + 1 in seq13))):
			true += 1

			#print indices_directory[i]

	#for i in range(9,18):
		#for j in indices_directory[i]:
		#	total +=1
		#	if(j[0] + 1 in seq13 and j[1] + 1 in seq13):
		#		true += 1
		#	if((not (j[0] + 1 in seq13)) and (not(j[1] + 1 in seq13))):
		#		true += 1

	#print indices_directory
	print float(true)/total


#compare.plot_data(FILTERED_ARRAYS)


