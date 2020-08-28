# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 00:15:22 2020

@author: nikhi
"""

# Script to convert yolo annotations to voc format

# Sample format
# <annotation>
#     <folder>_image_fashion</folder>
#     <filename>brooke-cagle-39574.jpg</filename>
#     <size>
#         <width>1200</width>
#         <height>800</height>
#         <depth>3</depth>
#     </size>
#     <segmented>0</segmented>
#     <object>
#         <name>head</name>
#         <pose>Unspecified</pose>
#         <truncated>0</truncated>
#         <difficult>0</difficult>
#         <bndbox>
#             <xmin>549</xmin>
#             <ymin>251</ymin>
#             <xmax>625</xmax>
#             <ymax>335</ymax>
#         </bndbox>
#     </object>
# <annotation>
import os
import xml.etree.cElementTree as ET
from PIL import Image
from math import floor

ANNOTATIONS_DIR_PREFIX = "G:/My Drive/ML_DL_Stuff/Object Detection/Datasets/OID_text/"
IMAGE_DIR_PREFIX = "G:/My Drive/ML_DL_Stuff/Object Detection/Datasets/OID_images/"
imgExt = "jpg"
imgChnls = 3 #RGB:3 ; Grayscale:1
DESTINATION_DIR = "G:/My Drive/ML_DL_Stuff/Object Detection/Datasets/converted_labels"

CLASS_MAPPING = {     '0' : 'Tomato', 
                      '1' : 'Bread',
     '2' : 'Milk',
     '3' : 'Knife',
     '4' : 'Broccoli',
     '5' : 'Cheese',
     '6' : 'Fork',
     '7' : 'Plate',
     '8' : 'Table',
     '9' : 'Mixing_bowl',
     '10' : 'Carrot',
     '11' : 'Turkey',
     '12' : 'Cookie',
     '13' : 'Coffee_cup',
     '14' : 'Platter'

    # Add your remaining classes here.
}


def create_root(file_prefix, width, height):
    root = ET.Element("annotations")
    ET.SubElement(root, "filename").text = "{}.jpg".format(file_prefix)
    ET.SubElement(root, "folder").text = "images"
    size = ET.SubElement(root, "size")
    ET.SubElement(size, "width").text = str(width)
    ET.SubElement(size, "height").text = str(height)
    ET.SubElement(size, "depth").text = "3"
    return root


def create_object_annotation(root, voc_labels):
    for voc_label in voc_labels:
        obj = ET.SubElement(root, "object")
        ET.SubElement(obj, "name").text = voc_label[0]
        ET.SubElement(obj, "pose").text = "Unspecified"
        ET.SubElement(obj, "truncated").text = str(0)
        ET.SubElement(obj, "difficult").text = str(0)
        bbox = ET.SubElement(obj, "bndbox")
        ET.SubElement(bbox, "xmin").text = str(voc_label[1])
        ET.SubElement(bbox, "ymin").text = str(voc_label[2])
        ET.SubElement(bbox, "xmax").text = str(voc_label[3])
        ET.SubElement(bbox, "ymax").text = str(voc_label[4])
    return root


def create_file(file_prefix, width, height, voc_labels):
    root = create_root(file_prefix, width, height)
    root = create_object_annotation(root, voc_labels)
    tree = ET.ElementTree(root)
    tree.write("{}/{}.xml".format(DESTINATION_DIR, file_prefix))


def read_file(file_path):
    file_prefix = file_path.split(".txt")[0]
    image_file_name = "{}.{}".format(file_prefix,imgExt)
    img = Image.open("{}/{}".format(IMAGE_DIR_PREFIX, image_file_name))
    print(img)

    w, h = img.size
    prueba = "{}/{}".format(ANNOTATIONS_DIR_PREFIX, file_path)
    print(prueba)
    with open(prueba) as file:
        lines = file.readlines()
        voc_labels = []
        for line in lines:	
            voc = []
            line = line.strip()
            data = line.split()
            voc.append(CLASS_MAPPING.get(data[0]))
            bbox_width = float(data[3]) * w
            bbox_height = float(data[4]) * h
            center_x = float(data[1]) * w
            center_y = float(data[2]) * h
            voc.append(floor(center_x - (bbox_width / 2)))
            voc.append(floor(center_y - (bbox_height / 2)))
            voc.append(floor(center_x + (bbox_width / 2)))
            voc.append(floor(center_y + (bbox_height / 2)))
            voc_labels.append(voc)
        create_file(file_prefix, w, h, voc_labels)
    print("Processing complete for file: {}".format(file_path))


def start():
    if not os.path.exists(DESTINATION_DIR):
        os.makedirs(DESTINATION_DIR)
    for filename in os.listdir(ANNOTATIONS_DIR_PREFIX):
        if filename.endswith('txt'):
            try:
                PathFileName = "{}/{}".format(ANNOTATIONS_DIR_PREFIX, filename)
                if os.stat(PathFileName).st_size > 0:
                    print("Si")
                    read_file(filename) 
            except:
                print("No")         
            
        else:
            print("Skipping file: {}".format(filename))


if __name__ == "__main__":
    start()