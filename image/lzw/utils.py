def log(*args, **kwargs):
    print(*args, **kwargs)

def ensure(condition, error_msg):
    if not condition :
        log(error_msg)

def ensureEqual(result, expected, error_msg):
    if result != expected :
        log(error_msg)

