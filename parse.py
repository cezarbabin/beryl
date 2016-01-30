import re
import numpy as np
import math
from scipy import linalg
import sys
#from visual import *

bvh_file = ""
mode = "CMU"
#mode = ""


def identifier(scanner, token):  return "IDENT", token
def operator(scanner, token):    return "OPERATOR", token
def digit(scanner, token):       return "DIGIT", token
def open_brace(scanner, token):  return "OPEN_BRACE", token
def close_brace(scanner, token): return "CLOSE_BRACE", token

#VARIABLES
current_token = 0
frame_count = 0
root_name = ""
#DATA STRUCTURES
skeleton = {}
translation = []
bone_context = []
motion_channels = []
motions = []
#diction = {}
time_series = {}
global_position = []
root_name = ""


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
    (r"[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?", digit),
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
	global root_name
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
	frame_time = 0.0
	motions = [ () ] * frame_count

	current_token = current_token + 1

	motion_channels.insert(0, ("HipPos", "SomeDirection"))
	motion_channels.insert(0, ("HipPos", "SomeDirection"))
	motion_channels.insert(0, ("HipPos", "SomeDirection"))
	motion_channels.insert(0, (root_name, "SomeDirection"))
	motion_channels.insert(0, (root_name, "SomeDirection"))
	motion_channels.insert(0, (root_name, "SomeDirection"))

	for i in range(0, frame_count):

		channel_values = []
		for channel in motion_channels:
			#if (i == 0):
				#print bvh[current_token][1]
			channel_values.append((channel[0], channel[1], float(bvh[current_token][1])))
			current_token = current_token + 1
		
		motions[i] = (frame_time, channel_values)

		frame_time = frame_time + frame_rate

def sin(x):
	return math.sin(math.radians(x))

def cos(x):
	return math.cos(math.radians(x))

def print_motions():
	global translation

	rotations = [ () ] * frame_count

	for i in range(0, frame_count):
		t = 0;
		for index in range(0, len(motion_channels)/3):

			z = motions[i][1][index*3][2]
			x = motions[i][1][index*3 + 1][2]
			y = motions[i][1][index*3 + 2][2]

			name = motion_channels[index*3][0]

			if (name != "HipPos"):
			
				offsets = np.array(skeleton[name]['offsets'])

				#print skeleton[name]['parent']

				val = rotation_matrix(z,x,y,offsets)
				
				translation[i][name] = val


def rotation_matrix(z, x, y, offsets):
	identity = np.array([[1.,0.,0],[0.,1.,0.],[0.,0.,1.]])
	Z = np.array([[cos(z),-sin(z),0],[sin(z), cos(z), 0], [0,0,1]]);
	X = np.array([[1, 0, 0],[0, cos(x), -sin(x)], [0, sin(x), cos(x)]]);
	Y = np.array([[cos(y), 0, sin(y)], [0, 1, 0], [-sin(y), 0, cos(y)]]);
	val = Z.dot(identity)
	val = X.dot(val)
	val = Y.dot(val)

	#tvector = np.array([0,0,0,1])

	#print val#.dot(t)
	
	#val = np.vstack([np.c_[val,offsets], tvector])
	
	return val

def calculate_animation():
	frame_count = len(translation)
	#print motions[0][1][0][0]
	rec_traversal(1, "me")

# Recursive function that calculates the global position of each vertex
def rec_traversal(frame_number, name):
	
	for i in range(0, 2):
		directory = translation[i]

		#find the ancestors 
		for index in range(2, len(motion_channels)/3):
			current = motions[i][1][index*3][0]
			#print current, skeleton[current]['parent']


			#look up the parent and skeleton and compute all the way up

def initial_skeleton(frame_number):
	#traverse the entire skeleton and create points using the offset 
	points = []
	segments = []
	diction = {}
	for index in range(0, len(motion_channels)/3):
		if (index == 1):
			continue
		name = motions[0][1][index*3][0]
		offset = skeleton[name]['offsets']
		parent = skeleton[name]['parent']

		#print "Name is " + name 

		#print "Offsets are "
		#print (offset[0], offset[1], offset[2])

		

		if (index == 0):
			x = motions[frame_number][1][index*3][2]
			y = motions[frame_number][1][index*3 + 1][2]
			z = motions[frame_number][1][index*3 + 2][2]
			pos = np.array([x, y, z])
			#print point
			#print translation[frame_number][name]

			#point = np.add(pos, offset)
			point = np.dot(pos, translation[frame_number][name])
			point = np.add(pos, offset)
			#print point
			
		else:
			#print "HERE"
			

			#print "Parent is" + parent
			#print "Parent position is " 
			#print (diction[parent][0], diction[parent][1], diction[parent][2])
			
			#point = np.add(diction[parent], offset)
			point = np.dot(diction[parent], translation[frame_number][name])
			point = np.add(pos, offset)
			

			#print x
			#print "Position is "
			#print (x, y, z)
			
			#print point
				
			#print point

		#print point
		points.append(point)
		if (parent != None):
			segments.append((point, diction[parent]))
		diction[name] = point
	#print points
	#graph(points)
	graph2(segments, frame_number)
	return points




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

def graph(arr):
	#c = color.red

	for i in arr:
		i1 = i[0]/50
		i2 = i[1]/50
		i3 = i[2]/50
		#print (i1,i2,i3)
		ball1 = sphere(make_trail = true, pos = (i1,i2,i3), radius = 0.05, color=color.red)
		#c = curve(pos = (a[0], a[1], a[2]), radius=0.05)
	
	#a = vector(0.1,0,0)

	#while True:
		#rate(10)
		#ball1.pos = ball1.pos + a
		#c.append(pos = ball1.pos)
		#if (ball1.pos[0] > 6):
			#ball1.color = color.yellow

def graph2(arr, nr):

	colors = [
	#reddish colors
	(1.00, 0.00, 0.00),(1.00, 0.03, 0.00),(1.00, 0.05, 0.00),(1.00, 0.07, 0.00),(1.00, 0.10, 0.00),(1.00, 0.12, 0.00),(1.00, 0.15, 0.00),(1.00, 0.17, 0.00),(1.00, 0.20, 0.00),(1.00, 0.23, 0.00),(1.00, 0.25, 0.00),(1.00, 0.28, 0.00),(1.00, 0.30, 0.00),(1.00, 0.33, 0.00),(1.00, 0.35, 0.00),(1.00, 0.38, 0.00),(1.00, 0.40, 0.00),(1.00, 0.42, 0.00),(1.00, 0.45, 0.00),(1.00, 0.47, 0.00),
	#orangey colors
	(1.00, 0.50, 0.00),(1.00, 0.53, 0.00),(1.00, 0.55, 0.00),(1.00, 0.57, 0.00),(1.00, 0.60, 0.00),(1.00, 0.62, 0.00),(1.00, 0.65, 0.00),(1.00, 0.68, 0.00),(1.00, 0.70, 0.00),(1.00, 0.72, 0.00),(1.00, 0.75, 0.00),(1.00, 0.78, 0.00),(1.00, 0.80, 0.00),(1.00, 0.82, 0.00),(1.00, 0.85, 0.00),(1.00, 0.88, 0.00),(1.00, 0.90, 0.00),(1.00, 0.93, 0.00),(1.00, 0.95, 0.00),(1.00, 0.97, 0.00),
	#yellowy colors
	(1.00, 1.00, 0.00),(0.95, 1.00, 0.00),(0.90, 1.00, 0.00),(0.85, 1.00, 0.00),(0.80, 1.00, 0.00),(0.75, 1.00, 0.00),(0.70, 1.00, 0.00),(0.65, 1.00, 0.00),(0.60, 1.00, 0.00),(0.55, 1.00, 0.00),(0.50, 1.00, 0.00),(0.45, 1.00, 0.00),(0.40, 1.00, 0.00),(0.35, 1.00, 0.00),(0.30, 1.00, 0.00),(0.25, 1.00, 0.00),(0.20, 1.00, 0.00),(0.15, 1.00, 0.00),(0.10, 1.00, 0.00),(0.05, 1.00, 0.00),
	#greenish colors
	(0.00, 1.00, 0.00),(0.00, 0.95, 0.05),(0.00, 0.90, 0.10),(0.00, 0.85, 0.15),(0.00, 0.80, 0.20),(0.00, 0.75, 0.25),(0.00, 0.70, 0.30),(0.00, 0.65, 0.35),(0.00, 0.60, 0.40),(0.00, 0.55, 0.45),(0.00, 0.50, 0.50),(0.00, 0.45, 0.55),(0.00, 0.40, 0.60),(0.00, 0.35, 0.65),(0.00, 0.30, 0.70),(0.00, 0.25, 0.75),(0.00, 0.20, 0.80),(0.00, 0.15, 0.85),(0.00, 0.10, 0.90),(0.00, 0.05, 0.95),
	#blueish colors
	(0.00, 0.00, 1.00),(0.05, 0.00, 1.00),(0.10, 0.00, 1.00),(0.15, 0.00, 1.00),(0.20, 0.00, 1.00),(0.25, 0.00, 1.00),(0.30, 0.00, 1.00),(0.35, 0.00, 1.00),(0.40, 0.00, 1.00),(0.45, 0.00, 1.00),(0.50, 0.00, 1.00),(0.55, 0.00, 1.00),(0.60, 0.00, 1.00),(0.65, 0.00, 1.00),(0.70, 0.00, 1.00),(0.75, 0.00, 1.00),(0.80, 0.00, 1.00),(0.85, 0.00, 1.00),(0.90, 0.00, 1.00),(0.95, 0.00, 1.00)
	]

	for i,j in arr:
		i1 = i[0]/50
		i2 = i[1]/50
		i3 = i[2]/50

		j1 = j[0]/50
		j2 = j[1]/50
		j3 = j[2]/50

		L = curve(pos=[(i1,i2,i3), (j1,j2,j3)], radius=0.005)#, color=colors[nr])

def cos(x):
	return math.cos(math.radians(x))

def print_motions():
	global translation
	print len(motion_channels)
	rotations = [ () ] * frame_count

	
	if (mode == "CMU"):
		#######################################################
		## Frame count
		#######################################################
		for i in range(0, frame_count):
			t = 0;

			for index in range(0, len(motion_channels)/3):
				z = motions[i][1][index*3][2]
				y = motions[i][1][index*3 + 1][2]
				x = motions[i][1][index*3 + 2][2]
				name = motion_channels[index*3][0]
				
				if (name == "HipPos"):
					name = root_name
				offsets = np.array(skeleton[name]['offsets'])
				val = rotation_matrix(z,y,x,offsets)
				translation[i][name] = val
	else:
		#######################################################
		## Frame count
		#######################################################
		for i in range(0, frame_count):
			t = 0;

			for index in range(0, len(motion_channels)/6):
				y = motions[i][1][index*6 + 3][2]
				x = motions[i][1][index*6 + 4][2]
				z = motions[i][1][index*3 + 5][2]
				name = motion_channels[index*6][0]
				
				if (name == "HipPos"):
					name = root_name
				offsets = np.array(skeleton[name]['offsets'])
				val = rotation_matrix(z,y,x,offsets)
				translation[i][name] = val


def rotation_matrix(z, y, x, offsets):
	identity = np.array([[1.,0.,0],[0.,1.,0.],[0.,0.,1.]])
	Z = np.array([[cos(z),-sin(z),0],[sin(z), cos(z), 0], [0,0,1]]);
	X = np.array([[1, 0, 0],[0, cos(x), -sin(x)], [0, sin(x), cos(x)]]);
	Y = np.array([[cos(y), 0, sin(y)], [0, 1, 0], [-sin(y), 0, cos(y)]]);
	val = Y.dot(identity)
	val = X.dot(val)
	val = Z.dot(val)	
	return val

def initial_skeleton(frame_number):
	diction = {}
	global global_position
	#traverse the entire skeleton and create points using the offset
	points = []
	segments = []
	if (mode == "CMU"):
		joints_number = len(motion_channels)/3
	else:
		joints_number = len(motion_channels)/6

	if(frame_number == 0):
		global_position = [()] * frame_count

	offset = skeleton[root_name]['offsets']
	x = motions[frame_number][1][0][2]
	y = motions[frame_number][1][1][2]
	z = motions[frame_number][1][2][2]
	pos = np.array([x, y, z])
	pos = np.add(pos, offset)
	point = np.dot(pos, translation[frame_number][root_name])
		
	diction[root_name] = [point[0], point[1], point[2]]

	for index in range(1, joints_number):
		if (index == 1 and mode == "CMU"):
			continue
		
		if (mode == "CMU"):
			name = motions[0][1][index*3][0]
		else:
			name = motions[0][1][index*6][0]

		offset = skeleton[name]['offsets']
		parent = skeleton[name]['parent']
		
		pos = np.add(diction[parent], offset)
		point = np.dot(pos, translation[frame_number][name])
		
		points.append(point)
		
		if (parent != None):
			segments.append((point, diction[parent]))

		diction[name] = [point[0], point[1], point[2]]
	
	global_position[frame_number] = diction
	return points

def triangular_mapping(joints_arr, nr):
	global diction
	global time_series
	segments = []
	joints_temp = ["Neck", "RightShoulder", "LeftUpLeg"]
	joints_arr = joints_temp
	print diction['Neck']
	time_series = {}
	areas = []
	for j in joints_arr:
		time_series[j] = []
		time_series[j].append(diction[j])
	x = time_series[joints_arr[0]][len(time_series[joints_arr[0]])-1]
	y = time_series[joints_arr[1]][len(time_series[joints_arr[1]])-1]
	z = time_series[joints_arr[2]][len(time_series[joints_arr[2]])-1]
	segments.append((x, y))
	segments.append((x, z))
	segments.append((y, z))
	area = np.add(x, y)
	area = np.add(area, z)
	areas.append(area)
	graph2(segments, nr)
	print skeleton

def graph(arr):
	#c = color.red
	for i in arr:
		i1 = i[0]/50
		i2 = i[1]/50
		i3 = i[2]/50
		#print (i1,i2,i3)
		ball1 = sphere(make_trail = true, pos = (i1,i2,i3), radius = 0.05, color=color.red)
		#c = curve(pos = (a[0], a[1], a[2]), radius=0.05)
	#a = vector(0.1,0,0)
	#while True:
		#rate(10)
		#ball1.pos = ball1.pos + a
		#c.append(pos = ball1.pos)
		#if (ball1.pos[0] > 6):
			#ball1.color = color.yellow

def graph2(arr, nr):
	colors = [
	#reddish colors
	(1.00, 0.00, 0.00),(1.00, 0.03, 0.00),(1.00, 0.05, 0.00),(1.00, 0.07, 0.00),(1.00, 0.10, 0.00),(1.00, 0.12, 0.00),(1.00, 0.15, 0.00),(1.00, 0.17, 0.00),(1.00, 0.20, 0.00),(1.00, 0.23, 0.00),(1.00, 0.25, 0.00),(1.00, 0.28, 0.00),(1.00, 0.30, 0.00),(1.00, 0.33, 0.00),(1.00, 0.35, 0.00),(1.00, 0.38, 0.00),(1.00, 0.40, 0.00),(1.00, 0.42, 0.00),(1.00, 0.45, 0.00),(1.00, 0.47, 0.00),
	#orangey colors
	(1.00, 0.50, 0.00),(1.00, 0.53, 0.00),(1.00, 0.55, 0.00),(1.00, 0.57, 0.00),(1.00, 0.60, 0.00),(1.00, 0.62, 0.00),(1.00, 0.65, 0.00),(1.00, 0.68, 0.00),(1.00, 0.70, 0.00),(1.00, 0.72, 0.00),(1.00, 0.75, 0.00),(1.00, 0.78, 0.00),(1.00, 0.80, 0.00),(1.00, 0.82, 0.00),(1.00, 0.85, 0.00),(1.00, 0.88, 0.00),(1.00, 0.90, 0.00),(1.00, 0.93, 0.00),(1.00, 0.95, 0.00),(1.00, 0.97, 0.00),
	#yellowy colors
	(1.00, 1.00, 0.00),(0.95, 1.00, 0.00),(0.90, 1.00, 0.00),(0.85, 1.00, 0.00),(0.80, 1.00, 0.00),(0.75, 1.00, 0.00),(0.70, 1.00, 0.00),(0.65, 1.00, 0.00),(0.60, 1.00, 0.00),(0.55, 1.00, 0.00),(0.50, 1.00, 0.00),(0.45, 1.00, 0.00),(0.40, 1.00, 0.00),(0.35, 1.00, 0.00),(0.30, 1.00, 0.00),(0.25, 1.00, 0.00),(0.20, 1.00, 0.00),(0.15, 1.00, 0.00),(0.10, 1.00, 0.00),(0.05, 1.00, 0.00),
	#greenish colors
	(0.00, 1.00, 0.00),(0.00, 0.95, 0.05),(0.00, 0.90, 0.10),(0.00, 0.85, 0.15),(0.00, 0.80, 0.20),(0.00, 0.75, 0.25),(0.00, 0.70, 0.30),(0.00, 0.65, 0.35),(0.00, 0.60, 0.40),(0.00, 0.55, 0.45),(0.00, 0.50, 0.50),(0.00, 0.45, 0.55),(0.00, 0.40, 0.60),(0.00, 0.35, 0.65),(0.00, 0.30, 0.70),(0.00, 0.25, 0.75),(0.00, 0.20, 0.80),(0.00, 0.15, 0.85),(0.00, 0.10, 0.90),(0.00, 0.05, 0.95),
	#blueish colors
	(0.00, 0.00, 1.00),(0.05, 0.00, 1.00),(0.10, 0.00, 1.00),(0.15, 0.00, 1.00),(0.20, 0.00, 1.00),(0.25, 0.00, 1.00),(0.30, 0.00, 1.00),(0.35, 0.00, 1.00),(0.40, 0.00, 1.00),(0.45, 0.00, 1.00),(0.50, 0.00, 1.00),(0.55, 0.00, 1.00),(0.60, 0.00, 1.00),(0.65, 0.00, 1.00),(0.70, 0.00, 1.00),(0.75, 0.00, 1.00),(0.80, 0.00, 1.00),(0.85, 0.00, 1.00),(0.90, 0.00, 1.00),(0.95, 0.00, 1.00)
	]
	for i,j in arr:
		i1 = i[0]/50
		i2 = i[1]/50
		i3 = i[2]/50
		j1 = j[0]/50
		j2 = j[1]/50
		j3 = j[2]/50
		#L = curve(pos=[(i1,i2,i3), (j1,j2,j3)], radius=0.005, color=colors[nr])

def motion_data(file_name, mode_input):
	global mode
	mode = mode_input
	main(file_name)
	return global_position

def reset():
	current_token = 0
	frame_count = 0
	root_name = ""
	#DATA STRUCTURES
	skeleton = {}
	translation = []
	bone_context = []
	motion_channels = []
	motions = []
	diction = {}
	time_series = {}
	global_position = []

def main(file_name):
	global bvh_file
	global bvh
	global tokens
	global current_token
	global frame_count

	bvh_file = file_name + ".bvh"
	bvh_file = open(bvh_file, "r")
	bvh = bvh_file.read()
	bvh_file.close()
	tokens, remainder = scanner.scan(bvh)
	parse_hierarchy(tokens)

	a = np.array([1,2,3])
	b = np.array([[0,0,0,6],[0,0,0,4],[0,0,0,6]])

	current_token = current_token + 1
	print current_token
	parse_motion(tokens)
	print_motions()

	#calculate_animation()
	#scene1 = display(title = "Mocap", x = 0, y =0, width = 800, height = 600, range = 10,
		#background=color.white)
	print frame_count

	#######################################################
	## Frame count
	#######################################################

	for i in range(0, frame_count):
		initial_skeleton(i)
	#motion_data(file_name)
	

if __name__ == "__main__":
	#main('02_01')
	motion_data('02_01')

	calculate_animation()

	scene1 = display(title = "Mocap", x = 0, y =0, width = 800, height = 600, range = 10,
		background=color.white)


	#print root_name
	for i in range(0, 180):
		initial_skeleton(i)





	
