# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 20:38:44 2020

@author: nikhi
"""

import sys
import os
import glob
import cv2

def convert_coco_to_yolo(left, top, width, height, img_width, img_height): 
  ## "c" stands for center and "n" stands for normalized
  half_width = float(width) / 2
  half_height = float(height) / 2
  ## compute left, top, right, bottom
  x_c = float(left) + half_width
  y_c = float(top) + half_height
  width_n = width/img_width
  height_n = height/img_height
  x_c_n = x_c/img_width
  y_c_n = y_c/img_height
  return x_c_n, y_c_n, width_n, height_n

def convert_yolo_coordinates_to_voc(x_c_n, y_c_n, width_n, height_n, img_width, img_height):
  ## remove normalization given the size of the image
  x_c = float(x_c_n) * img_width
  y_c = float(y_c_n) * img_height
  width = float(width_n) * img_width
  height = float(height_n) * img_height
  ## compute half width and half height
  half_width = width / 2
  half_height = height / 2
  ## compute left, top, right, bottom
  ## in the official VOC challenge the top-left pixel in the image has coordinates (1;1)
  left = int(x_c - half_width) + 1
  top = int(y_c - half_height) + 1
  right = int(x_c + half_width) + 1
  bottom = int(y_c + half_height) + 1
  return left, top, right, bottom


# make sure that the cwd() in the beginning is the location of the python script (so that every path makes sense)
os.chdir(os.path.dirname(os.path.abspath(__file__)))


# change directory to the one with the files to be changed

GT_PATH = '/home/ngunti/coco/labels/val2017/'
#print(GT_PATH)
os.chdir(GT_PATH)


# create VOC format files
txt_list = glob.glob('*.txt')
if len(txt_list) == 0:
  print("Error: no .txt files found in ground-truth")
  sys.exit()
for tmp_file in txt_list:
  #print(tmp_file)
  
  # 2. open txt file lines to a list
  with open(tmp_file) as f:
    content = f.readlines()
  ## remove whitespace characters like `\n` at the end of each line
  content = [x.strip() for x in content]
  # 4. create new file (YOLO format)
  with open(tmp_file, "w") as new_f:
    for line in content:
      ## split a line by spaces.
      ## "c" stands for center and "n" stands for normalized
      obj_id, left, top, width_n, height_n = line.split()
      #obj_name = obj_list[int(obj_id)]
      x_c_n, y_c_n, width_n, height_n = convert_coco_to_yolo(left, top, width_n, height_n)
      ## add new line to file
      #print(obj_name + " " + str(left) + " " + str(top) + " " + str(right) + " " + str(bottom))
      new_f.write(obj_id + " " + str(x_c_n) + " " + str(y_c_n) + " " + str(width_n) + " " + str(height_n) + '\n')
print("Conversion completed!")