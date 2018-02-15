import os
import os.path as path
import sys
from glob import glob

from src.pred.cli import decode as pred_decode
from src.pred.cli import encode as pred_encode
from src.video.cli import decode as video_decode
from src.video.cli import encode as video_encode


class DotDict(dict):
    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, val):
        if key in self.__dict__:
            self.__dict__[key] = val
        else:
            self[key] = val


def encoding_paths(intra_path):
    base = path.abspath(path.join(intra_path, '../..'))
    vblock = 'tmp/vblock'
    diff = 'tmp/diff'
    video = 'video/'
    paths = {
        'images': path.dirname(intra_path),
        'vblock': path.join(base, vblock),
        'diff': path.join(base, diff),
        'video': path.join(base, video),
    }
    return DotDict(paths)


def decoding_paths(davi_path, images_dir):
    base = path.abspath(path.join(davi_path, '../..'))
    vblock = 'tmp/vblock'
    diff = 'tmp/diff'
    video = path.dirname(davi_path)
    paths = {
        'intra': path.join(images_dir, 'big_buck_bunny_07501.png'),
        'images': images_dir,
        'vblock': path.join(base, vblock),
        'diff': path.join(base, diff),
        'video': video,
    }
    return DotDict(paths)


def setup_paths(paths):
    for k, v in paths.items():
        if k == 'intra':
            continue
        elif not os.path.exists(v):
            os.makedirs(v)
    pass


def next_path(prev_path):
    b = int(prev_path[-9:-4]) + 1
    c = str(b).zfill(5)
    d = 'big_buck_bunny_{}.png'.format(c)
    e = path.join(path.dirname(prev_path), d)
    return e


def encode(intra_path, davi_path):
    paths = encoding_paths(intra_path)
    setup_paths(paths)
    filenames = glob(path.join(paths.images, '*.png'))
    length = len(filenames)
    for i, _ in enumerate(filenames):
        if i + 1 < length:
            prev_path = filenames[i]
            curr_path = filenames[i + 1]
            pred_encode(prev_path, curr_path, paths.vblock, paths.diff)
    video_encode(intra_path, paths.vblock, paths.diff, davi_path)
    pass


def next_name(i):
    b = 7501 + i
    c = str(b).zfill(5)
    d = 'big_buck_bunny_{}'.format(c)
    return d
    pass


def decode(davi_path, images_dir):
    paths = decoding_paths(davi_path, images_dir)
    setup_paths(paths)
    video_decode(davi_path, images_dir)
    prev_path = paths.intra
    numbers_of_vblock = len(glob(path.join(paths.vblock, '*.vblock')))
    i = 1
    while i <= numbers_of_vblock:
        name = next_name(i)
        vblock_path = path.join(paths.vblock, name + '.vblock')
        diff_path = path.join(paths.diff, name + '.diff.png')
        pred_path = path.join(paths.images, name + '.png')
        pred_decode(prev_path, vblock_path, diff_path, pred_path)
        prev_path = pred_path
        i += 1
    pass


def cli():
    args = sys.argv[1:]
    if args[0] == 'encode':
        _, intra_path, davi_name = args
        encode(intra_path, davi_name)
    elif args[0] == 'decode':
        _, davi_path, images_dir = args
        decode(davi_path, images_dir)


if __name__ == '__main__':
    cli()
