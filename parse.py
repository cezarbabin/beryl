import re
import numpy as np
import math
from scipy import linalg

bvh_file = "Example1.bvh"

def identifier(scanner, token):  return "IDENT", token
def operator(scanner, token):    return "OPERATOR", token
def digit(scanner, token):       return "DIGIT", token
def open_brace(scanner, token):  return "OPEN_BRACE", token
def close_brace(scanner, token): return "CLOSE_BRACE", token

current_token = 0
frame_count = 0

skeleton = {}
translation = []
bone_context = []
motion_channels = []
motions = []

def new_bone(parent, name):
	bone = { "parent" : parent, "channels" : [], "offsets" : []}
	return bone

def push_bone_context(name):
	global bone_context
	bone_context.append(name)

def get_bone_context():
	global bone_context
	return bone_context[len(bone_context)-1]

def pop_bone_context():
	global bone_context
	bone_context = bone_context[:-1]
	return bone_context[len(bone_context)-1]

reserved      = [ "HIERARCHY", "ROOT", "OFFSET", "CHANNELS", "MOTION" ]
channel_names = [ "Xposition", "Yposition", "Zposition",  "Zrotation", "Xrotation",  "Yrotation" ]

scanner = re.Scanner([
    (r"[a-zA-Z_]\w*", identifier),
    (r"-*[0-9]+(\.[0-9]+)?", digit),
	(r"}", close_brace),
	(r"{", open_brace),
	(r":", None),
    (r"\s+", None),
    ])

def read_offset(bvh, token_index):
	if (bvh[token_index] != ("IDENT", "OFFSET")):
		return None, None
	token_index = token_index + 1
	offsets = [ 0.0 ] * 3
	for i in range(0,3):
		offsets[i] = float(bvh[token_index][1])
		token_index = token_index + 1
	return  offsets, token_index

def read_channels(bvh, token_index):
	if (bvh[token_index] != ("IDENT", "CHANNELS")):
		return None, None
	token_index = token_index + 1
	channel_count = int(bvh[token_index][1])
	token_index = token_index+1
	channels = [ "" ] * channel_count
	for i in range(0, channel_count):
		channels[i] = bvh[token_index][1]
		token_index = token_index+1
	return channels, token_index

def parse_joint(bvh, token_index):
	end_site = False
	joint_id = bvh[token_index][1]
	token_index = token_index + 1
	joint_name = bvh[token_index][1]
	token_index = token_index + 1
	if (joint_id == "End"): # end site
		joint_name = get_bone_context() + "_Nub"
		end_site = True
	joint = new_bone(get_bone_context(), joint_name)
	if bvh[token_index][0] != "OPEN_BRACE":
		print "Was expecting brace, got ", bvh[token_index]
		return None
	token_index = token_index + 1
	offsets, token_index = read_offset(bvh, token_index)
	joint["offsets"] = offsets
	if (not(end_site)):
		channels, token_index = read_channels(bvh, token_index)
		joint["channels"] = channels
		for channel in channels:
			motion_channels.append((joint_name, channel))
	skeleton[joint_name] = joint
	while (((bvh[token_index][0] == "IDENT") and (bvh[token_index][1] == "JOINT")) or
		  ((bvh[token_index][0] == "IDENT") and (bvh[token_index][1] == "End"))):
		push_bone_context(joint_name)
		token_index = parse_joint(bvh, token_index)
		pop_bone_context()
	if (bvh[token_index][0]) == "CLOSE_BRACE":
		return token_index + 1
	print "Unexpected token ", bvh[token_index]

def parse_hierarchy(bvh):
	global current_token
	current_token = 0
	if (bvh[current_token] != ("IDENT", "HIERARCHY")):
		return None
	current_token = current_token + 1
	if (bvh[current_token] != ("IDENT", "ROOT")):
		return None
	current_token = current_token + 1
	if (bvh[current_token][0] != "IDENT"):
		return None
	root_name =bvh[current_token][1]
	root_bone = new_bone(None, root_name)
	current_token = current_token + 1
	if bvh[current_token][0] != "OPEN_BRACE":
		return None
	current_token = current_token + 1
	offsets, current_token = read_offset(bvh, current_token)
	channels, current_token = read_channels(bvh, current_token)
	root_bone["offsets"]  = offsets
	root_bone["channels"] = channels
	skeleton[root_name] = root_bone
	push_bone_context(root_name)
	print "Root ", root_bone
	while(bvh[current_token][1] == "JOINT"):
		current_token = parse_joint(bvh, current_token)


def parse_motion(bvh):
	global current_token
	global frame_count
	global motions 
	global translation

	if (bvh[current_token][0] != "IDENT"):
		print "Unexpected text"
		return None
	if (bvh[current_token][1] != "MOTION"):
		print "No motion section"
		return None
	current_token = current_token + 1
	if (bvh[current_token][1] != "Frames"):
		return None
	current_token = current_token  + 1
	frame_count = int(bvh[current_token][1])
	current_token = current_token  + 1
	if (bvh[current_token][1] != "Frame"):
		return None
	current_token = current_token  + 1
	if (bvh[current_token][1] != "Time"):
		return None
	current_token = current_token + 1

	############# TEMPORARY FIX #######################

	translation = [ () ] * frame_count

	for i in range(0, frame_count):
		translation[i] = {}

	frame_rate = float(bvh[current_token][1])
	frame_time = 1
	motions = [ () ] * frame_count

	motion_channels.insert(0, ("HipPos", "SomeDirection"))
	motion_channels.insert(0, ("HipPos", "SomeDirection"))
	motion_channels.insert(0, ("HipPos", "SomeDirection"))
	motion_channels.insert(0, ("Hips", "SomeDirection"))
	motion_channels.insert(0, ("Hips", "SomeDirection"))
	motion_channels.insert(0, ("Hips", "SomeDirection"))

	for i in range(0, 3):

		channel_values = []
		for channel in motion_channels:
			channel_values.append((channel[0], channel[1], float(bvh[current_token][1])))
			current_token = current_token + 1
			print bvh[current_token][1], channel[0]
		motions[i] = (frame_time, channel_values)


		print "###################"
		frame_time = frame_time + 1

def update_hips(arr, frame_time):
	print arr
	
	px = float(arr[0])
	py = float(arr[1])
	pz = float(arr[2])
	z =  float(arr[3])
	x =  float(arr[4])
	y =  float(arr[5])

	translation[frame_time]['Hips']= rotation_matrix(z,x,y,skeleton["Hips"]['offsets'])


def sin(x):
	return math.sin(math.radians(x))

def cos(x):
	return math.cos(math.radians(x))

def print_motions():
	global translation

	rotations = [ () ] * frame_count

	for i in range(0, 3):
		t = 0;
		for index in range(0, len(motion_channels)/3):

			z = motions[i][1][index*3][2]
			x = motions[i][1][index*3 + 1][2]
			y = motions[i][1][index*3 + 2][2]

			name = motion_channels[index*3][0]

			if (name == "HipPos"):
				break
			offsets = np.array(skeleton[name]['offsets'])
			
			val = rotation_matrix(z,x,y,offsets)

			translation[i][name] = val


def store_matrix(vertex, matrix, parent, frame):
	dictionary = {}
	dictionary[vertex] = (matrix, parent, frame)

def calculate_animation():
	dictionary = {}
	for i in dictionary:
		matrix = [] #do the transpose and calculate vertex position through time
		# use rotation_matrix(m, m2)

def rotation_matrix(z, x, y, offsets):
	Z = np.array([[cos(z),-sin(z),0],[sin(z), cos(z), 0], [0,0,1]]);
	X = np.array([[1, 0, 0],[0, cos(x), -sin(x)], [0, sin(x), cos(x)]]);
	Y = np.array([[cos(y), 0, sin(y)], [0, 1, 0], [-sin(y), 0, cos(y)]]);

	val = Z.dot(X)
	val = val.dot(Y)

	tvector = np.array([0,0,0,1])

	#print val#.dot(t)
	
	val = np.vstack([np.c_[val,offsets], tvector])
	
	return val


	# perform vector operations that give us the Matrix rotation R
	# after that compute M using M = TR
	# after that get the vector value of the joint

#def triangle_area(joint1, joint2, joint3):
	# calculate the area using the formula specified in the presentation
	# record/store it somewhere in order to be able to use it for database lookups

#def chebyshev_center(joint1, joint2, joint3, joint4, ...):
	# find the chebyshev outer center and inner center and use it as a parameter

#def pca(m):
	# perform principal component analysis

#def joint_across_time(joint1):
	# use data from the joint in order to map it in 3D across time
	# use the change in color across time

#def bone_across_time(joint1):
	# use data from the two points connecting the joint and map it in 2 dimensions
	# across time
	# use change in color across time

#def cycle_detector(array_of_motion):
	# detects whether there is a cycle in the motion using triangle area and chebyshev center

#def keyframe_extractor(matrix_across_time):






if __name__ == "__main__":
	bvh_file = open(bvh_file, "r")
	bvh = bvh_file.read()
	bvh_file.close()
	tokens, remainder = scanner.scan(bvh)
	parse_hierarchy(tokens)
	#for (name,bone) in skeleton.iteritems():
	#	print "Bone " + name
	#	if bone.has_key("channels"):
	#		print "Channels ", bone["channels"]
	#	print "Offsets ", bone["offsets"]
	current_token = current_token + 1
	parse_motion(tokens)
	print_motions()
