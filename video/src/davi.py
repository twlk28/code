import os
import os.path as path
import sys

from src.pred.decode import decode2
import src.pred.encode as pred_encoder
import src.pred.decode as pred_decoder
import src.video.video as video_coder
from glob import glob
from src.video.video import Davi
from .utils import *
from PIL import Image
import io

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


def encode(intra_path, davi_name):
    paths = encoding_paths(intra_path)
    filenames = glob(path.join(paths.images, '*.png'))
    length = len(filenames)
    for i, _ in enumerate(filenames):
        if i + 1 < length:
            prev_path = filenames[i]
            curr_path = filenames[i+1]
            pred_encoder.encode(prev_path, curr_path, paths.vblock, paths.diff)
    #
    davi_path = path.join(paths.video, davi_name)
    video_coder.encode(intra_path, paths.vblock, paths.diff, davi_path)
    pass


def decode(davi_path, images_dir):
    davi = Davi.from_bytes(bytes_from_path(davi_path))
    # intra_frame
    intra_bytes = davi.diff[0]['data']
    intra_path = path.join(images_dir, '0.png')
    write_bytes(intra_bytes, intra_path)
    # pred_frame
    i = 1
    prev_bytes = intra_bytes
    while i < davi.frames:
        diff_bytes = davi.diff[i]['data']
        vblock_json = davi.vblock[i-1]
        pred_bytes = decode2(prev_bytes, vblock_json, diff_bytes)
        pred_path = path.join(images_dir, '{}.png'.format(i))
        write_bytes(pred_bytes, pred_path)
        prev_bytes = pred_bytes
        i += 1
    # paths = decoding_paths(davi_path, images_dir)
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
