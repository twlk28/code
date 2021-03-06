import io
import json


def write_json(jsondata, savepath):
    with open(savepath, 'w') as f:
        json1 = json.dumps(jsondata)
        f.write(json1)


def write_bytes(b, savepath):
    with open(savepath, 'wb') as f:
        f.write(b)


def json_from_path(p):
    data = None
    with open(p, encoding='utf-8') as f:
        data = json.load(f)
    return data


def bytes_from_path(p):
    d1 = None
    with open(p, 'rb') as f:
        d1 = f.read()
    return d1
    pass


def bytes_from_image(pil_img):
    img_bytes_io = io.BytesIO()
    pil_img.save(img_bytes_io, format='PNG')
    img_bytes = img_bytes_io.getvalue()
    return img_bytes
