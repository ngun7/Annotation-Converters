import os
import sys
import re
import os.path as osp
import json

from collections import OrderedDict

def get_image_id_from_path(image_path):
    image_path = osp.splitext(image_path)[0]
    m = re.search(r'\d+$', image_path)
    return int(m.group())


def create_results_entry(image_id, category_id, bbox, score):
    return OrderedDict({"image_id":image_id,
                        "category_id":category_id,
                        "bbox":bbox,
                        "score":score})

def load_class_names(path):
    with open(path) as f:
        return [line.rstrip("\n") for line in f.readlines()]

def write_json(input_txt, output_json, class_file, separator_key='Start processing', img_format='.jpg'):
    class_names = load_class_names(class_file)
    cls2id = {cls:id for id, cls in enumerate(class_names)}

    with open(output_json, 'w') as outfile:
        outfile.write('[')
        isReading = False

        with open(input_txt) as infile:
            for line in infile:
                if separator_key in line:
                    next(input_txt)
                    if img_format not in line:
                        break

                    # get text between two substrings (SEPARATOR_KEY and IMG_FORMAT)
                    image_path = re.search(separator_key + '(.*)' + img_format, line)
                    image_id = get_image_id_from_path(image_path.group(1))
                    
                    isReading = True
                elif isReading and ":" in line:
                    # split line on first occurrence of the character ':' and '%'
                    class_name, info = line.split(':', 1)
                    #class_name = class_name.replace(' ', '_')
                    confidence, bbox_info = info.split('%', 1)

                    # Found detection with same bbox with less class score (not best class)
                    if len(bbox_info) > 1:
                        # get all the coordinates of the bounding box
                        bbox_info = bbox_info.replace(')','') # remove the character ')'
                        bbox_info = bbox_info.split()

                        # go through each of the parts of the string and check if it is a digit
                        left, top, width, height = bbox_info[1], bbox_info[3], bbox_info[5], bbox_info[7]
                        right = left + width
                        bottom = top + height

                    category_id = cls2id[class_name]
                    bbox = [float(left), float(top), float(width), float(height)]
                    score = float(confidence) / 100

                    res = create_results_entry(image_id, category_id, bbox, score)
                    json.dump(res, outfile, indent=4, separators=(',', ':'))
                    outfile.write(',')

        # Remove trailing ',' and close the bracket
        outfile.seek(outfile.tell() - 1, os.SEEK_SET)
        outfile.truncate()
        outfile.write(']')
        outfile.close()





# outfile = None
# with open(IN_FILE) as infile:
#     for line in infile:
#         if SEPARATOR_KEY in line:
#             if IMG_FORMAT not in line:
#                 break
#             # get text between two substrings (SEPARATOR_KEY and IMG_FORMAT)
#             image_path = re.search(SEPARATOR_KEY + '(.*)' + IMG_FORMAT, line)
#             # get the image name (the final component of a image_path)
#             # e.g., from 'data/horses_1' to 'horses_1'
#             image_name = os.path.basename(image_path.group(1))
#             # close the previous file
#             if outfile is not None:
#                 outfile.close()
#             # open a new file
#             outfile = open(os.path.join(OUTPUT_DIR, image_name + '.txt'), 'w')
#         elif outfile is not None:
#             # split line on first occurrence of the character ':' and '%'
#             class_name, info = line.split(':', 1)
#             class_name = class_name.replace(' ', '_')
#             confidence, bbox = info.split('%', 1)
#             if len(bbox) != 1:
#                 # get all the coordinates of the bounding box
#                 bbox = bbox.replace(')','') # remove the character ')'
#                 # go through each of the parts of the string and check if it is a digit
#                 left, top, width, height = [int(s) for s in bbox.split() if s.lstrip('-').isdigit()]
#                 right = left + width
#                 bottom = top + height
#                 outfile.write("{} {} {} {} {} {}\n".format(class_name, float(confidence)/100, left, top, width, height))
#                 #outfile.write("{} {} {} {} {} {}\n".format(class_name, float(confidence)/100, left, top, right, bottom))
