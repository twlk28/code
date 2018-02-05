def log(*args, **kwargs):
    print(*args, **kwargs)

def ensure(condition, error_msg):
    if not condition :
        log(error_msg)

def ensureEqual(result, expected, error_msg):
    if result != expected :
        log(error_msg)

def bytes_from_path(path):
    s = []
    with open(path, 'rb') as f:
        s = f.read()
    return s


def write_to_path(path, raw):
    with open(path, 'wb') as f:
        f.write(bytes(raw))


def rename(path, suffix='rename'):
    a = path.split('.')
    a[-1] = suffix
    b = '.'.join(a)
    return b