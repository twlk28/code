from src.davi import encode, decode

if __name__ == '__main__':
    intra_path = '../sample/images/big_buck_bunny_07501.png'
    davi_name = 'out'
    encode(intra_path, davi_name)

    # vblock_path = '../sample/tmp/vblock/big_buck_bunny_07502.vblock'
    # diff_path = '../sample/tmp/diff/big_buck_bunny_07502.diff.png'
    # out_path = curr_path
    # decode(prev_path, vblock_path, diff_path, out_path)
    pass

'''
总入口
encode intra.png xx.davi -> generator xx.davi
-> intra.png ensure {image/ vblock/ diff/ video/}

decode xx.davi images/ -> images/*.png
-> 1.png ensure {image/ vblock/ diff/ video/}

--
video入口
encode
enocde intra.png vblock/ diff/ xx.davi -> xx.davi

decode
decode xx.davi images/ -> images/*.png

--
pred入口
encode
1.png 2.png -> 2.vblock 2.diff.png
encode 1.png 2.png vblock/ diff/

decode
1.png 2.vblock 2.diff.png -> 2.png
decode 1.png 2.vblock 2.diff.png images/2.png

'''

'''
路径相关
    path    a/b.davi
    dir     a/b/
    name    b.davi
    
文件类型
    intra   关键帧
    vblock, diff 中间产物
    davi    视频格式
    img     PIL 图片

'''