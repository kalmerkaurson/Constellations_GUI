from IPython import display
from PIL import Image, ImageDraw
import numpy as np
import tensorflow as tf
import sys
sys.path.insert(0, 'tpu/models/official')
sys.path.insert(0, 'tpu/models/official/mask_rcnn')
import coco_metric
from mask_rcnn.object_detection import visualization_utils

import os

ID_MAPPING = {
    1: 'person',
    2: 'bicycle',
    3: 'car',
    4: 'motorcycle',
    5: 'airplane',
    6: 'bus',
    7: 'train',
    8: 'truck',
    9: 'boat',
    10: 'traffic light',
    11: 'fire hydrant',
    13: 'stop sign',
    14: 'parking meter',
    15: 'bench',
    16: 'bird',
    17: 'cat',
    18: 'dog',
    19: 'horse',
    20: 'sheep',
    21: 'cow',
    22: 'elephant',
    23: 'bear',
    24: 'zebra',
    25: 'giraffe',
    27: 'backpack',
    28: 'umbrella',
    31: 'handbag',
    32: 'tie',
    33: 'suitcase',
    34: 'frisbee',
    35: 'skis',
    36: 'snowboard',
    37: 'sports ball',
    38: 'kite',
    39: 'baseball bat',
    40: 'baseball glove',
    41: 'skateboard',
    42: 'surfboard',
    43: 'tennis racket',
    44: 'bottle',
    46: 'wine glass',
    47: 'cup',
    48: 'fork',
    49: 'knife',
    50: 'spoon',
    51: 'bowl',
    52: 'banana',
    53: 'apple',
    54: 'sandwich',
    55: 'orange',
    56: 'broccoli',
    57: 'carrot',
    58: 'hot dog',
    59: 'pizza',
    60: 'donut',
    61: 'cake',
    62: 'chair',
    63: 'couch',
    64: 'potted plant',
    65: 'bed',
    67: 'dining table',
    70: 'toilet',
    72: 'tv',
    73: 'laptop',
    74: 'mouse',
    75: 'remote',
    76: 'keyboard',
    77: 'cell phone',
    78: 'microwave',
    79: 'oven',
    80: 'toaster',
    81: 'sink',
    82: 'refrigerator',
    84: 'book',
    85: 'clock',
    86: 'vase',
    87: 'scissors',
    88: 'teddy bear',
    89: 'hair drier',
    90: 'toothbrush',
}
category_index = {k: {'id': k, 'name': ID_MAPPING[k]} for k in ID_MAPPING}

def detect(np_image_string,width,height):
    # my modification
    session = tf.compat.v1.Session()#tf.Session()
    #First let's load meta graph and restore weights
    
    filename = os.path.dirname(os.path.abspath(__file__))+'\\savedmodel\\model\\my_test_model-1000.meta'
    filename = filename.replace("\\", "/")

    saver = tf.compat.v1.train.import_meta_graph(filename)#tf.train.import_meta_graph(filename)
    filename = os.path.dirname(os.path.abspath(__file__))+'\\savedmodel\\model\\'
    filename = filename.replace("\\", "/")
    saver.restore(session,tf.train.latest_checkpoint(filename+'./'))
    #session = tf.compat.v1.Session(graph=tf.Graph())
    #------------
    num_detections, detection_boxes, detection_classes, detection_scores, detection_masks, image_info = session.run(
        ['NumDetections:0', 'DetectionBoxes:0', 'DetectionClasses:0', 'DetectionScores:0', 'DetectionMasks:0', 'ImageInfo:0'],
        feed_dict={'Placeholder:0': np_image_string})

    num_detections = np.squeeze(num_detections.astype(np.int32), axis=(0,))
    detection_boxes = np.squeeze(detection_boxes * image_info[0, 2], axis=(0,))[0:num_detections]
    detection_scores = np.squeeze(detection_scores, axis=(0,))[0:num_detections]
    detection_classes = np.squeeze(detection_classes.astype(np.int32), axis=(0,))[0:num_detections]
    instance_masks = np.squeeze(detection_masks, axis=(0,))[0:num_detections]
    ymin, xmin, ymax, xmax = np.split(detection_boxes, 4, axis=-1)
    processed_boxes = np.concatenate([xmin, ymin, xmax - xmin, ymax - ymin], axis=-1)
    segmentations = coco_metric.generate_segmentation_from_masks(instance_masks, processed_boxes, height, width)
    return segmentations

def outline(image,segmentations,full):
    if(not full):
        if(len(segmentations)>2):
            seg = segmentations[0] + segmentations[1] + segmentations[2]
        elif (len(segmentations)>1):
            seg = segmentations[0] + segmentations[1]
        else:
            seg = segmentations[0]
        seg[np.where(seg>0) ]=1
        for l in range(3):
            image[:,:,l]= image[:,:,l]*seg
        edges_out = cv2.Canny(seg,1,1)
    image = cv2.blur(image, (3,3))
    edges = cv2.Canny(image,80,200)
    edges = edges | edges_out
    return edges
def draw_circle_white(draw,c,dist):
    r = dist
    shape = [(c[0]-r,c[1]-r),(c[0]+r,c[1]+r)]
    draw.ellipse(shape,fill=250)

def draw_circle_black(draw,c,dist):
    r = dist
    shape = [(c[0]-r,c[1]-r),(c[0]+r,c[1]+r)]
    draw.ellipse(shape,fill=0) 
    
def generate_image_dotted(edges,dist=40,dot= 2):
    im = Image.fromarray(edges)
    # create rectangle image 
    draw = ImageDraw.Draw(im)   
    img_shape = edges.shape
    px = im.load()
    for i in range(img_shape[0]):
        for j in range(img_shape[1]):
            if(px[j,i]==255):
                draw_circle_black(draw,(j,i),dist)
                px[j,i]=255
    for i in range(img_shape[0]):
        for j in range(img_shape[1]):
            if(px[j,i]==255):
                draw_circle_white(draw,(j,i),dot)
    return im

def add_noise(im,prob = 0.0001,dot =2 ):
    draw = ImageDraw.Draw(im)
    img_shape = np.array(im).shape
    for i in range(img_shape[0]):
        for j in range(img_shape[1]):
            if(np.random.random()<prob):
                draw_circle_white(draw,(j,i),dot)
    return np.array(im)

def save_image(image, base_folder, image_type, image_name):
    if not os.path.isdir(base_folder+'/'+image_type):
        os.mkdir(folder_path+'/'+image_type)
    plt.imsave(folder_path+'/'+image_type+'/'+image_name+'.jpg',image,cmap='gray')