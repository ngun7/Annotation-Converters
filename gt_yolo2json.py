import os
import sys
import re
import os.path as osp
import json
import cv2
import numpy as np
from tqdm import tqdm

from collections import OrderedDict

COCO_IDS = [1,2,3,4,5,6,7,8,9,10,11,13,14,15,16,17,18,19,20,21,22,23,24,25,27,28,31,32,33,34,35,36,37,38,39,40,41,42,43,44,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,67,70,72,73,74,75,76,77,78,79,80,81,82,84,85,86,87,88,89,90]



def create_annotations(cat_list, img_list, ann_list):
    return OrderedDict({'categories': cat_list,
                        'images': img_list,
                        'annotations': ann_list})

def create_images_entry(image_id, width=None, height=None):
    if width is None or height is None:
        return OrderedDict({'id':image_id })
    else:
        return OrderedDict({'id':image_id, 'width':width, 'height':height })

def create_categories(class_names, class_ids):
    return [{'id':class_ids[i], 'name':cls} for i, cls in enumerate(class_names)]

def create_annotations_entry(image_id, bbox, category_id, ann_id, iscrowd=0, area=None, segmentation=None):
    if area is None:
        if segmentation is None:
            #Calulate area with bbox
            area = bbox[2] * bbox[3]
        else:
            raise NotImplementedError()
            
    return OrderedDict({
            "id": ann_id,
            "image_id": image_id,
            "category_id": category_id,
            "iscrowd": iscrowd,
            "area": area,
            "bbox": bbox
           })


def get_image_id_from_path(image_path):
    image_path = osp.splitext(image_path)[0]
    m = re.search(r'\d+$', image_path)
    return int(m.group())

def bbox_cxcywh_to_xywh(box):
    x, y = box[..., 0] - box[..., 2] / 2, box[..., 1] - box[..., 3] / 2
    box[..., 0], box[..., 1] = x, y
    return box

def bbox_relative_to_absolute(box, img_dim, x_idx=[0,2], y_idx=[1,3]):
    box[..., x_idx] *= img_dim[0]
    box[..., y_idx] *= img_dim[1]
    return box

def get_img_ann_list(img_path_list, label_path_list, class_ids):
    img_list, ann_list = [],[]
    for img_path, label_path in tqdm(zip(img_path_list, label_path_list), file=sys.stdout, leave=True, total=len(img_path_list)):
        image_id = get_image_id_from_path(img_path)
        # Read Image
        if osp.exists(img_path):
            img = cv2.imread(img_path)
        
        height, width = img.shape[0], img.shape[1]
        img_list.append(create_images_entry(image_id, width, height))
        # Read Labels
        if osp.exists(label_path):
            labels = np.loadtxt(label_path).reshape(-1,5)
        labels[..., 1:5] = bbox_relative_to_absolute(bbox_cxcywh_to_xywh(labels[..., 1:5]), (width, height))
                                                     
        for label in labels:
            category_id = class_ids[int(label[0])]
            bbox = list(label[1:5])
            ann_id = len(ann_list)
            ann_list.append(create_annotations_entry(image_id, bbox, category_id, ann_id))
            
    return img_list, ann_list

def create_annotations_dict(target_txt, class_names, class_ids=None):
    if class_ids is None:
        class_ids = [i for i in range(len(class_names))]

    with open(target_txt, 'r') as f:
        img_path_list = [lines.strip() for lines in f.readlines()]
    label_path_list = [img_path.replace('jpg', 'txt').replace('images', 'labels') for img_path in img_path_list]
    
    #img_path_list, label_path_list = [img_path_list[1]], [label_path_list[1]]
    img_list, ann_list = get_img_ann_list(img_path_list, label_path_list, class_ids)
    cat_list = create_categories(class_names, class_ids)
    
    ann_dict = create_annotations(cat_list, img_list, ann_list)
        
    return ann_dict

def generate_annotations_file(target_txt, class_names, out, class_ids=None):
    ann_dict = create_annotations_dict(target_txt, class_names, class_ids=class_ids)
    with open(out, 'w') as f:
        json.dump(ann_dict, f, indent=4, separators=(',', ':'))