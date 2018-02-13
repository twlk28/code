from src.pred import pred

if __name__ == '__main__':
    prev_path = '../sample/images/big_buck_bunny_07501.png'
    curr_path = '../sample/images/big_buck_bunny_07502.png'
    vblock_dir = '../sample/tmp/vblock'
    diff_dir = '../sample/tmp/diff'
    pred.encode(prev_path, curr_path, vblock_dir, diff_dir)

    vblock_path = '../sample/tmp/vblock/big_buck_bunny_07502.vblock'
    diff_path = '../sample/tmp/diff/big_buck_bunny_07502.diff.png'
    out_path = curr_path
    pred.decode(prev_path, vblock_path, diff_path, out_path)
    pass

'''
总入口
encode 1.png 2.png
-> 1.png ensure {image/ vblock/ diff/ video/}

decode 1.png 2.vblock 2.diff.png
-> 1.png ensure {image/ vblock/ diff/ video/}

--
pred入口
encode
1.png 2.png -> 2.vblock 2.diff.png
encode 1.png 2.png vblock/ diff/

decode
1.png 2.vblock 2.diff.png -> 2.png
decode 1.png 2.vblock 2.diff.png images/2.png

'''