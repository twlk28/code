from src.video.video import encode

if __name__ == '__main__':
    intra_path = '../sample/images/big_buck_bunny_07501.png'
    vblock_dir = '../sample/tmp/vblock'
    diff_dir = '../sample/tmp/diff'
    davi_path = '../sample/video/out.davi'
    encode(intra_path, vblock_dir, diff_dir, davi_path)

    # vblock_path = '../sample/tmp/vblock/big_buck_bunny_07502.vblock'
    # diff_path = '../sample/tmp/diff/big_buck_bunny_07502.diff.png'
    # out_path = curr_path
    # decode(prev_path, vblock_path, diff_path, out_path)
    pass