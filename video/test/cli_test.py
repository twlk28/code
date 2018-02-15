import os

from src.cli import encode, decode


def setup():
    cwd = os.path.abspath(os.path.join(os.getcwd(), '../src'))
    os.chdir(cwd)


def test_encode():
    intra_path = '../sample/images/big_buck_bunny_07501.png'
    davi_path = '../sample/video/out.davi'
    encode(intra_path, davi_path)
    cmd = 'python3 cli encode {} {}'.format(intra_path, davi_path)
    os.system(cmd)
    pass


def test_decode():
    davi_path = '../sample/video/out.davi'
    images_dir = '../sample/sprite'
    decode(davi_path, images_dir)
    cmd = 'python3 cli decode {} {}'.format(davi_path, images_dir)
    os.system(cmd)
    pass


if __name__ == '__main__':
    setup()
    test_encode()
    test_decode()
    pass
