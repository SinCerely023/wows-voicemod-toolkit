
def slash_path(path: str) -> str:
    new_path = path
    while True:
        if new_path.find('\\\\') != -1:
            new_path = new_path.replace('\\\\', '\\')
        else:
            break
    new_path = new_path.replace('\\', '/')
    while True:
        if new_path.find('//') != -1:
            new_path = new_path.replace('//', '/')
        else:
            break
    return new_path


def anti_slash_path(path: str) -> str:
    new_path = path
    while True:
        if new_path.find('//') != -1:
            new_path = new_path.replace('/', '/')
        else:
            break
    new_path = new_path.replace('/', '\\')
    while True:
        if new_path.find('\\\\') != -1:
            new_path = new_path.replace('\\\\', '\\')
        else:
            break
    return new_path