import os.path as path

from PIL import Image

from src.utils import *


def grayimage(path):
    img = Image.open(path).convert('L')
    return img


def chunk_diff(pixels1, x1, y1, pixels2, x2, y2):
    sum = 0
    for j in range(0, 8):
        for i in range(0, 8):
            p1 = pixels1[x1 + i, y1 + j]
            p2 = pixels2[x2 + i, y2 + j]
            sum += abs(p1 - p2)
    return sum


def chunk_equal(pixels1, x1, y1, pixels2, x2, y2):
    # 比较8x8图块是否一致, xy是左上角的点
    threshold = 128
    sum = 0
    for j in range(0, 8):
        for i in range(0, 8):
            p1 = pixels1[x1 + i, y1 + j]
            p2 = pixels2[x2 + i, y2 + j]
            sum += abs(p1 - p2)
            if sum > threshold:
                return False
            else:
                continue
    return True


def coord_from_prev(img1, img2, x2, y2):
    # 找到 img2[x, y]块 在 img1 的定位
    scope = 8
    pixels1 = img1.load()
    pixels2 = img2.load()
    w, h = img1.size
    xmin, xmax = max(0, x2 - scope), min(w - 8, x2 + scope)
    ymin, ymax = max(0, y2 - scope), min(h - 8, y2 + scope)
    r = {
        'x': -1,
        'y': -1,
    }
    #
    diff = 9999
    for y1 in range(ymin, ymax):
        for x1 in range(xmin, xmax):
            if chunk_equal(pixels1, x1, y1, pixels2, x2, y2):
                r['x'] = x1
                r['y'] = y1
                return r
            else:
                diff2 = chunk_diff(pixels1, x1, y1, pixels2, x2, y2)
                if diff2 < diff:
                    diff = diff2
                    r['x'] = x1
                    r['y'] = y1
                continue
    return r


def vblock_gen(prev_img, curr_img):
    w, h = prev_img.size
    vblock = []
    for y in range(0, h, 8):
        for x in range(0, w, 8):
            r = coord_from_prev(prev_img, curr_img, x, y)
            vblock.append(r)
    return vblock


def interpolate_pixel(b, b1):
    return int((b1 - b) / 2 + 128)


def pixel_from_vblock(pixels, vblock, index, offset):
    x, y = vblock[index].values()
    y_delta, x_delta = offset // 8, offset % 8
    x += x_delta
    y += y_delta
    return pixels[x, y]
    pass


def diff_image_gen(vblock, prev_img, next_img):
    w, h = prev_img.size
    diff_img = Image.new('L', prev_img.size)
    diff_pixels = diff_img.load()
    prev_pixels = prev_img.load()
    next_pixels = next_img.load()
    for y in range(h):
        for x in range(w):
            x1, x2, y1, y2 = x // 8, x % 8, y // 8, y % 8
            index = y1 * int(w / 8) + x1
            offset = y2 * 8 + x2
            p1 = pixel_from_vblock(prev_pixels, vblock, index, offset)
            p2 = next_pixels[x, y]
            diff_pixels[x, y] = interpolate_pixel(p2, p1)
    return diff_img

def encode(prev_path, curr_path, vblock_dir, diff_dir):
    curr_name = path.basename(curr_path).split('.')[0]
    vblock_path = path.join(vblock_dir, curr_name + '.vblock')
    diff_path = path.join(diff_dir, curr_name + '.diff.png')
    curr_img = grayimage(curr_path)
    prev_img = grayimage(prev_path)
    #
    vblock = vblock_gen(prev_img, curr_img)
    write_json(vblock, vblock_path)
    #
    diff = diff_image_gen(vblock, prev_img, curr_img)
    diff.save(diff_path)
    pass

def encode2(prev_path, curr_path, paths):
    curr_name = path.basename(curr_path).split('.')[0]
    vblock_path = path.join(paths.vblock, curr_name + '.vblock')
    diff_path = path.join(paths.diff, curr_name + '.diff.png')
    curr_img = grayimage(curr_path)
    prev_img = grayimage(prev_path)
    #
    vblock = vblock_gen(prev_img, curr_img)
    write_json(vblock, vblock_path)
    #
    diff = diff_image_gen(vblock, prev_img, curr_img)
    diff.save(diff_path)
    pass
