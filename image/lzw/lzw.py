import sys

from decode import decode
from encode import encode
from utils import *


def cli():
    args = sys.argv[1:]
    coding = True if len(args) == 1 else False
    if coding:
        input_path = args[0]
        output_path = rename(input_path, 'lzw')
        encode(input_path, output_path)
    else:
        input_path = args[0]
        output_path = args[1]
        decode(input_path, output_path)


if __name__ == '__main__':
    cli()
