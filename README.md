# Times detector YOLOv2 Keras/Tensorflow

This repo contains an application of [YOLOv2 Keras/Tensorflow](https://github.com/experiencor/keras-yolo2.git) to times magazine detection.

## Dependencies:
- python            2.7.
- h5py              2.7.1
- imgaug            0.2.5
- Keras             2.1.5
- matplotlib        2.2.2
- affine            2.2.0
- numpy             1.14.2
- opencv-python     3.4.0.12
- Pillow            5.1.0
- pydot-ng          1.0.0
- tensorflow-gpu    1.7.0
- tqdm              4.23.0


## Description
The Yolo model for Time magazine detection was performed on Tesnsorflow-Keras using keras-yolo2. The training was performed with the base learning is 0.0001 and the batch size of 64. The current results were obtained by a max number of 10 plus 3 warm up epochs.

## Quick start / Installation:

-  setup/activate virtualenv
```
mkdir  ~/yolov2-keras
cd ~/yolov2-keras
virtualenv -p /usr/bin/python2.7 env
source env/bin/activate
```
- install dependencies
```
pip install numpy
pip install requests
pip install matplotlib
pip install affine
```

- install cv2
```
pip install opencv-python
```
- install imgaug from http://imgaug.readthedocs.io/en/latest/source/installation.html
```
pip install git+https://github.com/aleju/imgaug
```

- install tensorflow
```
pip install tensorflow-gpu
```

- install keras
```
pip install pydot_ng
pip install h5py
pip install pydot
pip install keras
```

- install tqdm
```
pip install tqdm
```
## 1. Synthetic images generation
500 Time magazine training images were generated by overlaying 5 random Time magazine cover image over 36 room background images. Times images were augmented by scaling, rotation and translation.
The object annotation were performed by [yolo_mark](https://github.com/AlexeyAB/Yolo_mark.git), generating annotation in VOC format. The source code for generating training images  are at ```./gen-times-images/igenerate_trainimgs.py```.

```
usage: generate_trainimgs.py [-h] [-n NUMBER_IMAGES] [-X WIDTH] [-Y HEIGHT]
                             [-j OBJECT_PATH] [-b BACKGROUND_PATH]
                             [-o OUTPUT_PATH] [-p PREFIX]

OR Train Image Generator.

optional arguments:
  -h, --help            show this help message and exit
  -n NUMBER_IMAGES, --number_images NUMBER_IMAGES
                        Number of images to generate. (default = 500)
  -X WIDTH, --width WIDTH
                        Width of images to generate. (default = 768)
  -Y HEIGHT, --height HEIGHT
                        height of images to generate. (default = 480)
  -j OBJECT_PATH, --object_path OBJECT_PATH
                        Path to object images. (default = './data/obj')
  -b BACKGROUND_PATH, --background_path BACKGROUND_PATH
                        Path to background images. (default = './data/bck')
  -o OUTPUT_PATH, --output_path OUTPUT_PATH
                        Path to output images. (default = './data/out')
  -p PREFIX, --prefix PREFIX
                        prefix to file name. (default = 'times-')

```

## 2. Train Yolo:
Train/valid configuration is set at ```./conf.json```.
The configuration is already set up for the current implementation.
Download pre-trained backend and full model weights from [here](https://1drv.ms/f/s!Avf8jJ1bO4r4aQbf57rKYI8UfqM). The weight files shall be placed at project root directory. The weight files are necessary to run the `train` and `predict_` codes.

```python
{
    "model" : {
        "backend":              "Full Yolo",
        "input_size":           416,
        "anchors":              [2.63, 5.17, 3.53, 4.98, 3.89, 6.42, 4.97, 5.84, 5.32, 7.04],
        "max_box_per_image":    10,
        "labels":               ["times"]
    },

    "train": {
        "train_image_folder":   "./data/times/train/images/",
        "train_annot_folder":   "./data/times/train/annots/",

        "train_times":          8,
        "pretrained_weights":   "",
        "batch_size":           16,
        "learning_rate":        1e-4,
        "nb_epochs":            10,
        "warmup_epochs":        3,

        "object_scale":         5.0 ,
        "no_object_scale":      1.0,
        "coord_scale":          1.0,
        "class_scale":          1.0,

        "saved_weights_name":   "full_yolo_times.h5",
        "debug":                true
    },

    "valid": {
        "valid_image_folder":   "./data/times/valid/images/",
        "valid_annot_folder":   "./data/times/valid/annots/",

        "valid_times":          1
    }
}
```

Train network by ```train.py```.
```
python train.py -c config.json
```
Trained weights will be saved at ```./full_yolo_times.h5```

```
usage: train.py [-h] [-c CONF]

Train and validate YOLO_v2 model on any dataset

optional arguments:
  -h, --help            show this help message and exit
  -c CONF, --conf CONF  path to configuration file

```

## 3. Perform detection:
- Perform detection on valid set. The current detection results are in ```./results/valid```
```
python predict_.py -c ./config.json -w ./full_yolo_times.h5 -i ./data/times/valid/images/ -o ./results/valid/
```
- Perform detection on train set. The current detection results are in ```./results/train```.
```
python predict_.py -c ./config.json -w ./full_yolo_times.h5 -i ./data/times/train/images/ -o ./results/train/
```
- Perform detection on video. The current detection results are in ```./video```
```
python predict_.py -c ./config.json -w ./full_yolo_times.h5 -i ./video/times-002.mp4
```

## 4. Evaluation:
The training convergence was monitored by valid Yolo Loss, and the weights model with lowest valid loss was saved .  In the current training, I do not see a big difference between train and validation loss, then no sign of over-fitting
![alt text](https://github.com/aidinraad/times-detector/blob/master/images/loss_plot.png)

## 5. To do:
- [ ] Add shear and perspective transformation.
- [ ] Add MAP checkpoint.

