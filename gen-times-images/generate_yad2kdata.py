

import os
import sys
import argparse
import numpy as np
try:
    from PIL import Image, ImageDraw
except ImportError:
    print("Install Pillow [`conda install pil`]!")
    sys.exit(1)


# define input args
argparser = argparse.ArgumentParser(description='Rename files sequentially.')

argparser.add_argument(
    '-i',
    '--images',
    help='Path to object images.',
    default=os.path.join('/home/aidin/work/codes/python/projects/gtimg/data/out2'))

argparser.add_argument(
    '-b',
    '--boxes',
    help='path to the objects ground truth boxes.',
    default=os.path.join('/home/aidin/work/codes/python/projects/gtimg/data/lbl/yolo2'))

argparser.add_argument(
    '-o',
    '--out',
    help='path to the output data.',
    default=os.path.join('/home/aidin/yad2k/data'))

argparser.add_argument(
    '-x',
    '--width',
    type=int,
    help='Width of images to generate.',
    default=768)

argparser.add_argument(
    '-y',
    '--height',
    type=int,
    help='height of images to generate.',
    default=480)


def printProgressBar(iteration,
                     total,
                     prefix='',
                     suffix='',
                     decimals=1,
                     length=100,
                     fill='█'):
    percent = ("{0:." + str(decimals) + "f}").format(
        100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r %s |%s| %s%% %s' %
        (prefix, bar, percent, suffix), end='\r')
    # Print New Line on Complete
    if iteration == total:
        print()
        

def read_boxes(fname, path, delimiter=' '):
    with open(os.path.join(path, fname)) as f:
        lines = f.readlines()
        boxes = []
        for line in lines:
            box = [float(x) for x in line.split(delimiter)]
            xc = box[1]
            yc = box[2]
            xmin = xc-box[3]/2
            ymin = yc-box[4]/2
            xmax = xc+box[3]/2
            ymax = yc+box[4]/2
            boxes += [box[0], xmin, ymin, xmax, ymax]
        return np.array(boxes)


def _main(args):
    """
    """
    path_img = os.path.expanduser(args.images)
    path_box = os.path.expanduser(args.boxes)
    path_out = os.path.expanduser(args.out)
    sz_trg = (args.width, args.height)


    assert os.path.isdir(path_img), '{} is not a valid path!'.format(path_img)
    assert os.path.isdir(path_box), '{} is not a valid path!'.format(path_box)
    assert os.path.isdir(path_out), '{} is not a valid path!'.format(path_out)

    fnames_img = sorted([f for f in os.listdir(path_img) if
                  os.path.isfile(os.path.join(path_img, f))])
    fnames_box = sorted([f for f in os.listdir(path_box) if
                  os.path.isfile(os.path.join(path_box, f))])
    
    n_imgs = len(fnames_img)
    printProgressBar(0, n_imgs, prefix='Progress:',
                     suffix='Complete', length=50)
    images = []
    boxes = []
    for i in range(len(fnames_img)):
        img = Image.open(os.path.join(path_img, fnames_img[i]))
        img = img.resize(sz_trg, Image.BICUBIC)
        box = read_boxes(fnames_box[i], path_box, delimiter=' ')


#        draw = ImageDraw.Draw(img)
#        draw.rectangle((box[1]*sz_trg[0], box[2]*sz_trg[1]) +
#                       (box[3]*sz_trg[0], box[4]*sz_trg[1]))
#        img.save('aaa', "PNG")

        images.append(np.array(img, dtype=np.uint8))
        boxes.append(box)
        printProgressBar(i+1, n_imgs, prefix='Progress:',
                         suffix='Complete', length=50)

    np.savez(os.path.join(path_out,'data'), images=images, boxes=boxes)


if __name__ == '__main__':
    """
    """
    args = argparser.parse_args()
    _main(args)
