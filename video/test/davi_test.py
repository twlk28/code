from src.davi import encode, decode

if __name__ == '__main__':
    intra_path = '../sample/images/big_buck_bunny_07501.png'
    davi_name = 'out.davi'
    encode(intra_path, davi_name)

    davi_path = '../sample/video/out.davi'
    images_dir = '../sample/sprite'
    decode(davi_path, images_dir)
    pass