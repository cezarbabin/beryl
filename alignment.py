
import parse 

#	figure out how to name the constants HIP | KNEE | SHOULDER
hip = "Hips"
lknee = "LeftLeg"
rknee = "RighLeg"
lshoulder = "LeftShoulder"
rshoulder = "RightShoulder"

######################################################################
#	This method is used in order to determine whether the movement is 
#	completely symmetric. We are looking to see if:
#	1.shoulders
#	2.knees
#	3.hips
#	are all moving in sync with each other
#
#
# 	look at the cyclicity parameters 
# 	look at the distance positionally across time
# 	look at the range in angles
######################################################################
# 	Primarily used for walking
######################################################################
def bodyDynamicAlignment(mat):
	arrays = get_joints(mat, hip, lknee, rknee, lshoulder, rshoulder)
	hip_arr = arrays[0]
	lknee_arr = arrays[1]
	rknee_arr = arrays[2]
	lshoulder = arrays[3]
	rshoulder = arrays[4]
	print " "

def jointDynamicAlignment(joint1, joint2, joint3):
	#	compare cycle value from joint 1 with value from joint 2
	coef1 = cycle.compute(joint1)
	coef2 = cycle.compute(joint2)

	amplitude1 = cycle.amplitude(joint1)
	amplitude2 = cycle.amplitude(joint2)

	#	compute score for deviation in distance 
	distance_arr = []
	for i in (len(joint1[0])):
		x = joint1[0][i] - joint2[0][i]
		y = joint1[1][i] - joint2[1][i]
		z = joint1[2][i] - joint2[2][i]
		distance_arr.append((x,y,z))
	return 0

def simultaneousMovement(joint1, joint2, joint3):
	#	look at joints functionally and see if they are moving simultaneously
	#	using their time-based x/y/z values
	coef1 = cycle.compute(joint1)
	amplitude1 = cycle.compute(joint1)

	coef2 = cycle.compute(joint2)
	amplitude2 = cycle.compute(joint2)

	coef3 = cycle.compute(joint3)
	amplitude3 = cycle.compute(joint3)
	return 0

	
######################################################################
#	Compute the alignment (positionally) and the foot placement
#	Will only get a couple of frames as reference
#	Likely to be a couple of moments right before the movement of
#	shoulder, elbow and wrist joints. As a result, need to detect 
#	when the "Burst" is happening and isolate that event and compute 
#	alighnment
######################################################################
# 	Primarily used for free-throw
######################################################################
def bodyPositionalAlignment(mat, errorMargin):
	#delta x,y,z knees	
	#delta x,y,z shoulders
	#delta x,y,z feet (feet placement)
	#in sum are they smaller than errorMargin ? 
	#return coeff
	print "Computed whether the shoulders are completely aligned x,y,z"

def jointPositionalAlignment(mat, errorMargin):
	#delta x
	
	#delta y

	#delta z

	#in sum are they smaller than errorMargin ? 

	#return coeff

	print "Computed whether the shoulders are completely aligned x,y,z"

def computeScore():
	print "the alignment score quantitatively but also qualitative assessment"

def get_joints(mat, nameA, nameB, nameC, nameD, nameE):
	mat1 = []
	mat2 = []
	mat3 = []
	mat4 = []
	mat5 = []

	mat1x = []
	mat1y = []
	mat1z = []
	mat2x = []
	mat2y = []
	mat2z = []
	mat3x = []
	mat3y = []
	mat3z = []
	mat4x = []
	mat4y = []
	mat4z = []
	mat5x = []
	mat5y = []
	mat5z = []

	for i in range(0, len(mat)):
		mat1x.append(mat[i][nameA][0])
		mat1y.append(mat[i][nameA][1])
		mat1z.append(mat[i][nameA][2])
		mat2x.append(mat[i][nameB][0])
		mat2y.append(mat[i][nameB][1])
		mat2z.append(mat[i][nameB][2])
		mat3x.append(mat[i][nameC][0])
		mat3y.append(mat[i][nameC][1])
		mat3z.append(mat[i][nameC][2])
		mat4x.append(mat[i][nameD][0])
		mat4y.append(mat[i][nameD][1])
		mat4z.append(mat[i][nameD][2])
		mat5x.append(mat[i][nameE][0])
		mat5y.append(mat[i][nameE][1])
		mat5z.append(mat[i][nameE][2])

	#print mat1
	mat1.append(mat1x)
	mat1.append(mat1y)
	mat1.append(mat1z)

	mat2.append(mat2x)
	mat2.append(mat2y)
	mat2.append(mat2z)

	mat3.append(mat3x)
	mat3.append(mat3y)
	mat3.append(mat3z)

	mat4.append(mat4x)
	mat4.append(mat4y)
	mat4.append(mat4z)

	mat5.append(mat5x)
	mat5.append(mat5y)
	mat5.append(mat5z)

	return (mat1, mat2, mat3, mat4, mat5)


if __name__ == '__main__':
	arr1 = parse.motion_data('02_01')
	reload(parse)
	arr2 = parse.motion_data('07_01')
	#compare.main(arr1, arr2, "rFoot", "rFoot")
