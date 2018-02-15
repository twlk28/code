import os.path as path
import sys

import src.pred.decode as pred_decoder
import src.pred.encode as pred_encoder
from src.utils import *


def encode(prev_path, curr_path, vblock_dir, diff_dir):
    curr_name = path.basename(curr_path).split('.')[0]
    prev_bytes = bytes_from_path(prev_path)
    curr_bytes = bytes_from_path(curr_path)
    vblock, diff = pred_encoder.encode(prev_bytes, curr_bytes)
    vblock_path = path.join(vblock_dir, curr_name + '.vblock')
    write_json(vblock, vblock_path)
    diff_path = path.join(diff_dir, curr_name + '.diff.png')
    write_bytes(diff, diff_path)
    pass


def decode(prev_path, vblock_path, diff_path, opath):
    prev_bytes = bytes_from_path(prev_path)
    vblock_json = json_from_path(vblock_path)
    diff_bytes = bytes_from_path(diff_path)
    pred_bytes = pred_decoder.decode(prev_bytes, vblock_json, diff_bytes)
    write_bytes(pred_bytes, opath)
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
