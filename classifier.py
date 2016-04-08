import re
import numpy as np
import math
from scipy import linalg
import sys

# Takes in an array of x,y,z positions for all 9 joints and outputs an
# average of the x,y positions within 10 intervals of ~equal size for each joint
# 
# Input: joints --> an array of 9 joints objects in the order
# [RightShoulder, RightArm, RightForearm, RightHand, LeftShoulder, LeftArm, LeftForearm, LeftHand, Head]
#    each joint object is an array of n (x,y,z) positions where n is the number of frames
#
# Output: A num_intervals*9*2 matrix (called A) where every array of 9 size(2) arrays represents the average position (x,y)
# of each joint for one interval. There are num_intervals such arrays representing each interval.
def populateA(joints):
  num_intervals = 10
  A = [[(0,0) for x in range(num_intervals)] for x in range(9)]
  tot_num_frames = len(joints[0])
  #print "Total Number of Frames: " + str(tot_num_frames)
  frames_per_interval = tot_num_frames/float(num_intervals)
  #print "Frames Per Interval (w/ decimal): " + str(frames_per_interval)
  frames_per_small_interval = int(math.floor(frames_per_interval))
  #print "Frames Per Small Interval: " + str(frames_per_small_interval)
  num_larger_intervals = num_intervals*(float(frames_per_interval-frames_per_small_interval))
  num_larger_intervals = int(math.ceil(num_larger_intervals))
  #print "Number of Large Intervals: " + str(num_larger_intervals)
  for j in range(0,9):
    joint = joints[j-1]
    #print "Currently processing joint at index: " + str(j-1)
    cur_frame = 0
    for i in range(0,num_intervals):
      num_frames = frames_per_small_interval
      x_pos_sum = 0
      y_pos_sum = 0
      #z_pos_sum = 0
      for k in range(1,frames_per_small_interval):
        x_pos_sum += joint[cur_frame][0]
        y_pos_sum += joint[cur_frame][1]
        #z_pos_sum += joint[cur_frame][2]
        cur_frame+= 1
      if i <= num_larger_intervals:
        num_frames = frames_per_small_interval + 1
        x_pos_sum += joint[cur_frame][0]
        y_pos_sum += joint[cur_frame][1]
        #z_pos_sum += joint[cur_frame][2]
        cur_frame+=1
        #print "This is a large interval"
      #else:
        #print "This is a small interval"
      #print "Interval has this number of frames: " + str(num_frames)
      #print "Current frame: " + str(cur_frame)
      x_pos_avg = x_pos_sum/num_frames
      y_pos_avg = y_pos_sum/num_frames
      #print "x_pos_sum: " + str(x_pos_sum)
      #print "x_pos_avg: " + str(x_pos_avg)
      #print "y_pos_sum: " + str(y_pos_sum)
      #print "y_pos_avg: " + str(y_pos_avg)
      #z_pos_avg = z_pos_sum/num_frames
      #index = (((i)*9)+j)
      #print "index: " + str(index)

      # This is an output with an array of 9 arrays, each of which contains an array of 10 tuples
      A[j][i] = (x_pos_avg,y_pos_avg)
  # This is an output that consists of one array containing 9 elements, each of which is a tuple of 20 elements.
  # The 9 elements correspond to the 9 joints; the 20 elements correspond to the (x1,y1,...,x10,y10) avg x and y
  # positions for the 10 intervals
  B = [0 for x in range(9)]
  for j in range(0,9):
    B[j] = sum(A[j], ())
    #print B[j]
  C = sum(B, ())
  return C

def createMatrix():
  z = 0
  A = [[(0,0) for x in range(10)] for x in range(9)]
  for j in range(0,9):
    for i in range(0,10):
      z += 1
      #print "i: " + str(i)
      #print "\nj: " + str(j) + "\n"
      #index = (((i)*9)+j)
      #print "Iteration: \n i: " + str(i) + "\n j: " + str(j)
      #print "Size: " + str(len(A[0]))
      #print A
      #print index
      print z
      A[j][i] = (j,i)
  B = [0 for x in range(9)]
  for j in range(0,9):
      B[j] = sum(A[j], ())
      print B[j]
  C = sum(B, ())
  return C

output = createMatrix()
print output
