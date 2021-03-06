import os
import os.path as path
import sys
from glob import glob

from PIL import Image

from src.pred.decode import decode as pred_decode
from src.pred.encode import encode as pred_encode
from src.video.video import Davi
from .utils import *


def setup_paths(p):
    if not os.path.exists(p):
        os.makedirs(p)


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
        'images': images_dir,
        'vblock': path.join(base, vblock),
        'diff': path.join(base, diff),
        'video': video,
    }
    return DotDict(paths)


def next_path(prev_path):
    b = int(prev_path[-9:-4]) + 1
    c = str(b).zfill(5)
    d = 'big_buck_bunny_{}.png'.format(c)
    e = path.join(path.dirname(prev_path), d)
    return e


def encode(intra_path, davi_path):
    davi = Davi()
    numbers_of_images = len(glob(path.join(path.dirname(intra_path), '*.png')))
    width, height = Image.open(intra_path).size
    davi.write_meta(numbers_of_images, width, height)
    intra_bytes = bytes_from_path(intra_path)
    davi.write_diff(intra_bytes)
    prev_path = intra_path
    prev_bytes = intra_bytes
    i = 1
    while i < numbers_of_images:
        curr_path = next_path(prev_path)
        curr_bytes = bytes_from_path(curr_path)
        vblock, diff_bytes = pred_encode(prev_bytes, curr_bytes)
        davi.write_diff(diff_bytes)
        davi.write_vblock(vblock)
        prev_path = curr_path
        prev_bytes = curr_bytes
        i += 1
    davi.save(davi_path)


def decode(davi_path, images_dir):
    setup_paths(images_dir)
    davi = Davi.from_bytes(bytes_from_path(davi_path))
    intra_bytes = davi.diff[0]['data']
    intra_path = path.join(images_dir, '0.png')
    write_bytes(intra_bytes, intra_path)
    i = 1
    prev_bytes = intra_bytes
    while i < davi.frames:
        diff_bytes = davi.diff[i]['data']
        vblock_json = davi.vblock[i - 1]
        pred_bytes = pred_decode(prev_bytes, vblock_json, diff_bytes)
        pred_path = path.join(images_dir, '{}.png'.format(i))
        write_bytes(pred_bytes, pred_path)
        prev_bytes = pred_bytes
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
