import os.path as path
import sys
from glob import glob

import PIL.Image as Image

from src.utils import *
from .video import Davi


class DotDict(dict):
    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, val):
        if key in self.__dict__:
            self.__dict__[key] = val
        else:
            self[key] = val


def next_diff_path(prev_path):
    b = int(prev_path[-14:-9]) + 1
    c = str(b).zfill(5)
    d = 'big_buck_bunny_{}.diff.png'.format(c)
    e = path.join(path.dirname(prev_path), d)
    return e


def next_vblock_path(prev_path):
    b = int(prev_path[-12:-7]) + 1
    c = str(b).zfill(5)
    d = 'big_buck_bunny_{}.vblock'.format(c)
    e = path.join(path.dirname(prev_path), d)
    return e


def encoding_paths(intra_path):
    base = path.abspath(path.join(intra_path, '../..'))
    vblock = 'tmp/vblock'
    diff = 'tmp/diff'
    video = 'video/'
    paths = {
        'intra': intra_path,
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


def decode(davi_path, images_dir):
    davi = Davi.from_bytes(bytes_from_path(davi_path))
    paths = decoding_paths(davi_path, images_dir)
    write_bytes(davi.diff[0]['data'], paths.intra)
    diff_path = path.join(paths.diff, 'big_buck_bunny_07501.diff.png')
    vblock_path = path.join(paths.vblock, 'big_buck_bunny_07501.vblock')
    i = 1
    while i < davi.frames:
        diff_bytes = davi.diff[i]['data']
        diff_path = next_diff_path(diff_path)
        write_bytes(diff_bytes, diff_path)
        vblock = davi.vblock[i - 1]
        vblock_path = next_vblock_path(vblock_path)
        write_json(vblock, vblock_path)
        i += 1
    pass


def encode(intra_path, vblock_dir, diff_dir, davi_path):
    davi = Davi()
    paths = encoding_paths(intra_path)
    numbers_of_images = len(glob(path.join(paths.images, '*.png')))
    width, height = Image.open(intra_path).size
    davi.write_meta(numbers_of_images, width, height)
    # intra
    davi.write_diff(bytes_from_path(intra_path))
    # diff
    for p in glob(path.join(paths.diff, '*.diff.png')):
        davi.write_diff(bytes_from_path(p))
    # vblock
    for p in glob(path.join(paths.vblock, '*.vblock')):
        davi.write_vblock(json_from_path(p))
    davi.save(davi_path)
    pass


def cli():
    args = sys.argv[1:]
    if args[0] == 'encode':
        _, intra_path, vblock_dir, diff_dir, davi_path = args
        encode(intra_path, vblock_dir, diff_dir, davi_path)
    elif args[0] == 'decode':
        _, davi_path, image_dir = args
        decode(davi_path, image_dir)
    pass


if __name__ == '__main__':
    cli()
