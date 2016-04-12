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


