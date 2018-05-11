

from __future__ import print_function
import sys
import os
import argparse
import numpy as np
try:
    from PIL import Image
except ImportError:
    print("Install Pillow [`conda install pil`]!")
    sys.exit(1)
try:
    from matplotlib.pyplot import imshow
except ImportError:
    print("Install matplotlib [`conda install matplotlib`]!")
    sys.exit(1)
try:
    from affine import Affine
except ImportError:
    print("Install affine [`conda install Affine`]!")
    sys.exit(1)


# define input args
argparser = argparse.ArgumentParser(
    description="OR Train Image Generator.")

argparser.add_argument(
    "-n",
    "--number_images",
    type=int,
    help="Number of images to generate. (default = 500)",
    default=500)

argparser.add_argument(
    "-X",
    "--width",
    type=int,
    help="Width of images to generate. (default = 768)",
    default=768)

argparser.add_argument(
    "-Y",
    "--height",
    type=int,
    help="height of images to generate. (default = 480)",
    default=480)

argparser.add_argument(
    "-j",
    "--object_path",
    help="Path to object images. (default = './data/obj')",
    default=os.path.join('./', 'data/obj'))

argparser.add_argument(
    "-b",
    "--background_path",
    help="Path to background images. (default = './data/bck')",
    default=os.path.join('./', 'data/bck'))

argparser.add_argument(
    "-o",
    "--output_path",
    help="Path to output images. (default = './data/out')",
    default=os.path.join('./', 'data/out'))

argparser.add_argument(
    "-p",
    "--prefix",
    help="prefix to file name. (default = 'times-')",
    default="times-")


def printProgressBar(iteration,
                     total,
                     prefix='',
                     suffix='',
                     decimals=1,
                     length=100,
                     fill="="):
    percent = ("{0:." + str(decimals) + "f}").format(
        100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + "-" * (length - filledLength)
    print("\r%s |%s| %s%% %s" % (prefix, bar, percent, suffix), end='\r')
    # Print New Line on Complete
    if iteration == total:
        print()


def affine_transform(img,
                     angle=0.,
                     scale=(1., 1.),
                     expand=True):

    # scale image
    img = img.resize((int(img.size[0]*scale[0]), int(img.size[1]*scale[1])))
    # rotate image
    img = img.rotate(angle, expand=expand)
    return img


def perspective_transform(img, m=-0.5):
    width, height = img.size
    xshift = abs(m) * width
    new_width = width + int(round(xshift))
    img = img.transform((new_width, height),
                        Image.AFFINE,
                        (1, m, -xshift if m > 0 else 0, 0, 1, 0),
                        Image.BICUBIC)
    return img


def add_objimg(wsz_bck, hsz_bck, fname_obj, fname_bck, fname_out):
    """
    """
    img_obj = Image.open(fname_obj)
    img_bck = Image.open(fname_bck)

    img_bck = img_bck.resize((wsz_bck, hsz_bck))
    
    hrt = 0.6
    hsz_obj = int(img_bck.size[1] * hrt)
    wsz_obj = int(img_obj.size[0] * hsz_obj / img_obj.size[1])

    img_obj = img_obj.resize((wsz_obj, hsz_obj))
    msk_obj = Image.new('RGBA', (wsz_obj, hsz_obj), color=(255, 255, 255, 255))

    theta_min = -90
    theta_max = 90
    theta = theta_min + (theta_max-theta_min)*np.random.random()

    sx_min = 0.5
    sx_max = .9
    sx = sx_min + (sx_max-sx_min)*np.random.random()
    xy = sx
    img_obj = affine_transform(img_obj,
                               angle=theta,
                               scale=(sx, xy),
                               expand=True)
    msk_obj = affine_transform(msk_obj,
                               angle=theta,
                               scale=(sx, xy),
                               expand=True)

    tx_min = int(max(img_obj.size))
    tx_max = img_bck.size[0] - int(max(img_obj.size))
    ty_min = int(max(img_obj.size))
    ty_max = img_bck.size[1] - int(max(img_obj.size))
    tx = tx_min + (tx_max-tx_min)*np.random.random()
    ty = ty_min + (ty_max-ty_min)*np.random.random()

    box = (0+int(tx), 0+int(ty))
    img_bck.paste(img_obj, box, msk_obj)
    img_bck.save(fname_out)


def _main(args):
    """
    """
    n_imgs = args.number_images
    w = args.width
    h = args.height
    path_obj = os.path.expanduser(args.object_path)
    path_bck = os.path.expanduser(args.background_path)
    path_out = os.path.expanduser(args.output_path)
    prefix = os.path.expanduser(args.prefix)

    assert os.path.isdir(path_obj), '{} is not a valid path!'.format(path_obj)
    assert os.path.isdir(path_bck), '{} is not a valid path!'.format(path_bck)
    assert os.path.isdir(path_out), '{} is not a valid path!'.format(path_out)

    fnames_obj = [f for f in os.listdir(path_obj) if
                  os.path.isfile(os.path.join(path_obj, f))]
    fnames_bck = [f for f in os.listdir(path_bck) if
                  os.path.isfile(os.path.join(path_bck, f))]

    printProgressBar(0, n_imgs, prefix='Progress:',
                     suffix='Complete', length=50)
    for i in range(n_imgs):
        fname_obj = fnames_obj[np.random.randint(0, len(fnames_obj)-1)]
        fname_bck = fnames_bck[np.random.randint(0, len(fnames_bck)-1)]
        fname_out = '{:s}{:05d}.jpg'.format(prefix, i)

        add_objimg(w, h, 
                   os.path.join(path_obj, fname_obj),
                   os.path.join(path_bck, fname_bck),
                   os.path.join(path_out, fname_out))
        printProgressBar(i+1, n_imgs, prefix='Progress:',
                         suffix='Complete', length=50)


if __name__ == '__main__':
    """
    """
    args = argparser.parse_args()
    _main(args)
