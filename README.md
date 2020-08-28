# Annotation-converters
This Repo covers all formats of annotations for Object Detection and can easily convert from one form to another using attached scripts 

All computer vision problems require annotated datasets and for training deep neural networks data needs to be annotated in defined form. For Object Detection, there are many available formats for preparing and annotating your dataset but the most popular and used formats are Pascal VOC and Microsoft COCO.

### MS COCO ###
COCO is large scale images with Common Objects in Context (COCO) for object detection, segmentation, and captioning data set. COCO has 1.5 million object instances for 80 object categories. COCO stores annotations in a JSON file.\
COCO Bounding box: _(x-top left, y-top left, width, height)_

### Pascal VOC ###
Pascal Visual Object Classes(VOC) provides standardized image data sets for object detection. Pascal VOC is an XML file, unlike COCO which has a JSON file.\
Pascal VOC Bounding box :_(xmin-top left, ymin-top left, xmax-bottom right, ymax-bottom right)_

### Darknet YOLO ###
YOLO reads or predicts bounding boxes in different format compared to VOC or COCO.\
YOLO Bounding box : _(x_center, y_center, width, height)_ --> all these coordinates are normalized with respect to image width & height.

In Pascal VOC and YOLO we create a file for each of the image in the dataset. In COCO we have one file each, for entire dataset for training, testing and validation.

Usually, when working on custom datasets we end up wasting lot of time in converting annotations from one format to another suitable to object detection models or frameworks. This is really frustrating and I compiled few annotations converter scripts which covers most of the cases and saves you time! You can now focus more on productive tasks such as improving model performance or training more efficiently.

## Scripts ##

* **JSON_to_txt.py**
  * It converts MS COCO JSON file to a text file for each image and the format is _{class_id, x_min, y_min, width, height}_


* **Yolo_to_Voc.py**
   * It converts YOLO text files to Pascal VOC format XML files
   * _(x_c_n, y_c_n, width_n, height_n) --> (x_min, y_min, x_max, y_max)_

* **XML_to_JSON.py** &&  **voc2coco.py**
  * These python scripts convert all XML files of a dataset into MS COCO readable JSON file.\
    `python XML_to_JSON.py ./annotations_dir/  ./json_dest_dir/coco_output.json`

* **gt_yolo2json.py**  && **pred_yolo2json.py**
  * It converts all YOLO text files into MS COCO readable JSON file.
  * For ground truth YOLO text files --> gt_yolo2json.py
  * For YOLO predicted text files --> pred_yolo2json.py

* **cocoGT_to_Yolo.py**
  * It converts MS COCO ground truth text files to YOLO format. It also has a function to convert YOLO text files to VOC format. Feel free to change the code and switch between the functions.
  
* **JSON --> VOC XML files**
  * Json2PascalVoc is a Python library for converting some special Json strings to PascalVOC format XML files.\
   `pip install Json2PascalVoc`
   ```
   from Json2PascalVoc.Converter import Converter
      
   myConverter = Converter()
   #returns a Converter Object
   myConverter.convertJsonToPascal("data.json")
   #Converts Json to PascalVOC XML and saves the XML file to the related file path
   ```
   
   
