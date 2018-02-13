import json

def write_json(jsondata, savepath):
    with open(savepath, 'w') as f:
        json1 = json.dumps(jsondata)
        f.write(json1)

def json_from_path(p):
    data = None
    with open(p, encoding='utf-8') as f:
        data = json.load(f)
    return data
