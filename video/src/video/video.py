import os.path as path
import sys
from glob import glob
from struct import pack

import PIL.Image as Image

from src.utils import *


class Davi(object):
    def __init__(self):
        self.meta = {}
        self.diff = []
        self.vblock = []
        self._setup_meta()
        pass

    def _setup_meta(self):
        self.meta['identifier'] = 'davi'
        self.meta['version'] = '1.0\n'
        pass

    def write_meta(self, frames, width, height):
        self.meta['frames'] = frames
        self.meta['width'] = width
        self.meta['height'] = height

    def write_diff(self, diff_bytes):
        item = {
            'size': len(diff_bytes),
            'data': diff_bytes,
        }
        self.diff.append(item)
        pass

    def write_vblock(self, vblock_json):
        self.vblock.append(vblock_json)
        pass

    def save(self, savepath):
        data = bytearray()

        # process meta
        d = {
            'identifier': '4s',
            'version': '4s',
            'frames': 'B',
            'width': 'H',
            'height': 'H',
        }
        for k, fmt in d.items():
            if fmt[-1] == 's':
                data += pack(fmt, self.meta[k].encode('ascii'))
            else:
                data += pack(fmt, self.meta[k])

        # process diff
        for o in self.diff:
            data += pack('I', o['size'])
            data += o['data']

        # process vblock
        for b in self.vblock:
            for pair in b:
                x, y = pair.values()
                data += pack('H', x)
                data += pack('H', y)

        # write out
        with open(savepath, 'wb') as f:
            f.write(data)
        pass


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


def encode(intra_path, vblock_dir, diff_dir, davi_path):
    davi = Davi()
    paths = encoding_paths(intra_path)
    numbers_of_images = len(glob(path.join(paths.images, '*.png')))
    width, height = Image.open(intra_path).size
    davi.write_meta(numbers_of_images, width, height)
    # write diff
    davi.write_diff(bytes_from_path(intra_path))
    for p in glob(path.join(paths.diff, '*.diff.png')):
        davi.write_diff(bytes_from_path(p))
    # write vblock
    for p in glob(path.join(paths.vblock, '*.vblock')):
        davi.write_vblock(json_from_path(p))
    davi.save(davi_path)
    pass


def decode(davi_path, images_dir):
    pass


def cli():
    args = sys.argv[1:]
    if args[0] == 'encode':
        _, intra_path, vblock_dir, diff_dir, davi_path = args
        encode(intra_path, vblock_dir, diff_dir, davi_path)
    elif args[0] == 'decode':
        pass
    pass


if __name__ == '__main__':
    cli()
