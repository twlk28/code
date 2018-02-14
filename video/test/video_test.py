from src.video.video import encode, decode

if __name__ == '__main__':
    intra_path = '../sample/images/big_buck_bunny_07501.png'
    vblock_dir = '../sample/tmp/vblock'
    diff_dir = '../sample/tmp/diff'
    davi_path = '../sample/video/out.davi'
    encode(intra_path, vblock_dir, diff_dir, davi_path)

    # davi_path = '../sample/video/out.davi'
    images_dir = '../sample/sprite'
    decode(davi_path, images_dir)
    pass