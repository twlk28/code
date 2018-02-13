import os
import os.path as path
import sys

import src.pred.decode as pred_decoder
import src.pred.encode as pred_encoder


class DotDict(dict):
    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, val):
        if key in self.__dict__:
            self.__dict__[key] = val
        else:
            self[key] = val


def paths_from_src(src):
    base = path.abspath(path.join(src, '../..'))
    vblock = 'tmp/vblock'
    diff = 'tmp/diff'
    out = 'out/'
    paths = {
        # 'base': base,
        'vblock': path.join(base, vblock),
        'diff': path.join(base, diff),
        'out': path.join(base, out),
    }
    return DotDict(paths)


def setup_paths(paths):
    for _, v in paths.items():
        if not os.path.exists(v):
            os.makedirs(v)
    pass


def encode(prev_path, curr_path, vblock_dir, diff_dir):
    # paths = paths_from_src(prev_path)
    pred_encoder.encode(prev_path, curr_path, vblock_dir, diff_dir)
    pass


def decode(prev_path, vblock_path, diff_path, opath):
    # paths = paths_from_src(prev_path)
    pred_decoder.decode(prev_path, vblock_path, diff_path, opath)
    pass


def cli():
    args = sys.argv[1:]
    if args[0] == 'encode':
        _, prev_path, curr_path, vblock_dir, diff_dir = args
        encode(prev_path, curr_path, vblock_dir, diff_dir)

    elif args[0] == 'decode':
        _, _, prev_path, vblock_path, diff_path, opath = args
        decode(prev_path, vblock_path, diff_path, opath)
    pass


if __name__ == '__main__':
    cli()
