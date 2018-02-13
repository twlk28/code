import os.path as path

from PIL import Image

from .utils import *


def grayimage(path):
    img = Image.open(path).convert('L')
    return img


def next_name(prev_path):
    b = int(prev_path[-9:-4]) + 1
    c = str(b).zfill(5)
    d = 'big_buck_bunny_{}'.format(c)
    return d


def pixel_from_vblock(pixels, vblock, index, offset):
    x, y = vblock[index].values()
    y_delta, x_delta = offset // 8, offset % 8
    x += x_delta
    y += y_delta
    return pixels[x, y]


def interpolate_pixel2(b, b1):
    x = b1 - (b - 128) * 2
    return x


def curr_img_gen(vblock, diff_img, prev_img):
    curr_img = Image.new('L', prev_img.size)
    prev_pixels, curr_pixels, diff_pixels = prev_img.load(), curr_img.load(), diff_img.load()
    w, h = prev_img.size
    for y in range(h):
        for x in range(w):
            x1, x2, y1, y2 = x // 8, x % 8, y // 8, y % 8
            index = y1 * int(w / 8) + x1
            offset = y2 * 8 + x2
            p1 = pixel_from_vblock(prev_pixels, vblock, index, offset)
            p2 = diff_pixels[x, y]
            p3 = interpolate_pixel2(p2, p1)
            curr_pixels[x, y] = p3
    return curr_img


def decode2(prev_path, paths):
    curr_name = next_name(prev_path)
    vblock_path = path.join(paths.vblock, curr_name + '.vblock')
    diff_path = path.join(paths.diff, curr_name + '.diff.png')
    out_path = path.join(paths.out, curr_name + '.png')
    vblock, diff_img, prev_img = json_from_path(vblock_path), grayimage(diff_path), grayimage(prev_path)
    curr_img = curr_img_gen(vblock, diff_img, prev_img)
    curr_img.save(out_path)
    pass

def decode(prev_path, vblock_path, diff_path, out_path):
    vblock, diff_img, prev_img = json_from_path(vblock_path), grayimage(diff_path), grayimage(prev_path)
    curr_img = curr_img_gen(vblock, diff_img, prev_img)
    curr_img.save(out_path)