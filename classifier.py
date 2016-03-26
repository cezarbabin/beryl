import re
import numpy as np
import math
from scipy import linalg
import sys

def populateA(joints):
  num_intervals = 10
  A = [[0,0]*90]
  #A = [9*num_intervals][2]
  tot_num_frames = len(joints[0])
  print "Total Number of Frames: " + str(tot_num_frames)
  frames_per_interval = tot_num_frames/float(num_intervals)
  print "Frames Per Interval (w/ decimal): " + str(frames_per_interval)
  frames_per_small_interval = int(math.floor(frames_per_interval))
  print "Frames Per Small Interval: " + str(frames_per_small_interval)
  num_larger_intervals = num_intervals*(float(frames_per_interval-frames_per_small_interval))
  num_larger_intervals = int(math.ceil(num_larger_intervals))
  print "Number of Large Intervals: " + str(num_larger_intervals)
  for j in range(1,9):
    joint = joints[j-1]
    print "Currently processing joint at index: " + str(j-1)
    cur_frame = 0
    for i in range(1,num_intervals):
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
        print "This is a large interval"
      else:
        print "This is a small interval"
      print "Interval has this number of frames: " + str(num_frames)
      print "Current frame: " + str(cur_frame)
      x_pos_avg = x_pos_sum/num_frames
      y_pos_avg = y_pos_sum/num_frames
      print "x_pos_sum: " + str(x_pos_sum)
      print "x_pos_avg: " + str(x_pos_avg)
      print "y_pos_sum: " + str(y_pos_sum)
      print "y_pos_avg: " + str(y_pos_avg)
      #z_pos_avg = z_pos_sum/num_frames
      index = (((i-1)*9)+j)-1
      print "index: " + str(index)
      A[index][0] = x_pos_avg
      A[index][1] = y_pos_avg
  return A