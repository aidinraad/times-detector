

import os
import argparse


# define input args
argparser = argparse.ArgumentParser(description='Rename files sequentially.')

argparser.add_argument(
    '-i',
    '--input_path',
    help='Path to input images.',
    default=os.path.join('./'))

argparser.add_argument(
    '-o',
    '--output_path',
    help='Path to renamed images.',
    default=os.path.join('./'))

argparser.add_argument(
    '-p',
    '--prefix',
    help='prefix to file names.',
    default='')


def _main(args):
    """
    """
    path_in = os.path.expanduser(args.input_path)
    path_out = os.path.expanduser(args.output_path)
    prefix = os.path.expanduser(args.prefix)

    assert os.path.isdir(path_in), '{} is not a valid path!'.format(path_in)
    assert os.path.isdir(path_out), '{} is not a valid path!'.format(path_out)

    fnames = [f for f in os.listdir(path_in) if
              os.path.isfile(os.path.join(path_in, f))]

    for i, fname in enumerate(fnames):
        fext = fname.split('.')[-1]
        print(fext)
        os.rename(
            os.path.join(path_in, fname),
            os.path.join(path_out, "{:s}{:05d}.{:s}".format(prefix, i, fext)))


if __name__ == '__main__':
    """
    """
    args = argparser.parse_args()
    _main(args)
