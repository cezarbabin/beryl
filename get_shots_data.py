import parse 
import compare
import classifier

MOTION_ARRAY = parse.motion_data('motion_files/fahim_11_Char00', "")

shots = []

for i in range(0,10):
	FILTERED_ARRAYS = compare.main(MOTION_ARRAY, compare.FT_JOINT_LIST, i)[1]

	shot = classifier.populateA(FILTERED_ARRAYS)

	shots.append[shot]

joint_shots = []
indices_directory = {}

for joint in range(0,9):
	for shot in shots:
		joint_shots.append(shot[joint])
	joint_indices = find_nearest_neighbors(joint_shots)
	indices_directory[joint] = joint_indices
	joint_shots = []

print indices_directory

def find_nearest_neighbors(arr):
	nbrs = NearestNeighbors(n_neighbors=2, algorithm='ball_tree').fit(arr)
	distances, indices = nbrs.kneighbors(arr)

	return indices 

#compare.plot_data(FILTERED_ARRAYS)


