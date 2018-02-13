import os.path as path
import sys


def paths_from_src(src):
    base = path.relpath(path.join(src, '..'))
    vblock = 'tmp/vblock'
    diff = 'tmp/diff'
    out = 'out/'
    paths = {
        # 'base': base,
        'vblock': path.join(base, vblock),
        'diff': path.join(base, diff),
        'out': path.join(base, out),
    }
    return paths


def cli():
    args = sys.argv[1:]
    if args[0] == 'encode':
        _, src, oname = args
        exec(src, oname)


if __name__ == '__main__':
    cli()
