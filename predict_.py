#! /usr/bin/env python

import argparse
import os
import cv2
import numpy as np
from tqdm import tqdm
from preprocessing import parse_annotation
from utils import draw_boxes
from frontend import YOLO
import json

os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"]="0"

argparser = argparse.ArgumentParser(
    description='Train and validate YOLO_v2 model on any dataset')

argparser.add_argument(
    '-c',
    '--conf',
    help='path to configuration file.')

argparser.add_argument(
    '-w',
    '--weights',
    help='path to pretrained weights.')

argparser.add_argument(
    '-i',
    '--input',
    help='path to input images or path to input video in mp4 format.')

argparser.add_argument(
    '-o',
    '--output',
    help='path to output images. Not required for video input.')

def _main_(args):
    config_path  = args.conf
    weights_path = args.weights
    input_path   = args.input
    output_path   = args.output

    with open(config_path) as config_buffer:    
        config = json.load(config_buffer)

    ###############################
    #   Make the model 
    ###############################

    yolo = YOLO(backend             = config['model']['backend'],
                input_size          = config['model']['input_size'], 
                labels              = config['model']['labels'], 
                max_box_per_image   = config['model']['max_box_per_image'],
                anchors             = config['model']['anchors'])

    ###############################
    #   Load trained weights
    ###############################    

    yolo.load_weights(weights_path)

    ###############################
    #   Predict bounding boxes 
    ###############################

    if input_path[-4:] == '.mp4':
        video_out = input_path[:-4] + '_detected' + input_path[-4:]
        video_reader = cv2.VideoCapture(input_path)

        nb_frames = int(video_reader.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_h = int(video_reader.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_w = int(video_reader.get(cv2.CAP_PROP_FRAME_WIDTH))

        video_writer = cv2.VideoWriter(video_out,
                               cv2.VideoWriter_fourcc(*'MPEG'), 
                               30.0, 
                               (frame_w, frame_h))

        for i in tqdm(range(nb_frames)[:-1]):
            _, image = video_reader.read()
            
            boxes = yolo.predict(image)
            image = draw_boxes(image, boxes, config['model']['labels'])

            video_writer.write(np.uint8(image))

        video_reader.release()
        video_writer.release()  
    else:
        fnames = sorted([f for f in os.listdir(input_path) if
                 os.path.isfile(os.path.join(input_path, f))])        
        for i, fname in enumerate(fnames):
            ffname = os.path.join(input_path, fname)
            ffname_ = os.path.join(
                output_path,
                fname[:-4] + '_detected' + fname[-4:])
            
            image = cv2.imread(ffname)
            boxes = yolo.predict(image)
            image = draw_boxes(image, boxes, config['model']['labels'])
            print(len(boxes), 'boxes are found')
            cv2.imwrite(ffname_, image)

if __name__ == '__main__':
    args = argparser.parse_args()
    _main_(args)
