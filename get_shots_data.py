import parse 
import compare
import classifier
from sklearn.neighbors import NearestNeighbors

#MOTION_ARRAY = parse.motion_data('motion_files/fahim_11_Char00', "")

def find_nearest_neighbors(arr):
	nbrs = NearestNeighbors(n_neighbors=2, algorithm='ball_tree').fit(arr)
	distances, indices = nbrs.kneighbors(arr)

	return indices 

def main(MOTION_ARRAY):
	shots = []

	for i in range(0,10):
		FILTERED_ARRAYS = compare.main(MOTION_ARRAY, compare.FT_JOINT_LIST, i)[1]

		shot = classifier.populateA(FILTERED_ARRAYS)

		shots.append(shot)

	joint_shots = []
	indices_directory = {}

	for joint in range(0,9):
		for shot in shots:
			joint_shots.append(shot[joint])
		joint_indices = find_nearest_neighbors(joint_shots)
		indices_directory[joint] = joint_indices
		joint_shots = []

	seq11 = [5,6,7,9]
	true = 0
	total = 0

	for i in indices_directory:
		for j in indices_directory[i]:
			total +=1
			if(j[0] in seq11 and j[1] in seq11):
				true += 1
			if((not (j[0] in seq11)) and (not(j[1] in seq11))):
				true += 1

			#print indices_directory[i]

	#print indices_directory
	print float(true)/total


#compare.plot_data(FILTERED_ARRAYS)


