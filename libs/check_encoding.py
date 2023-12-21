import chardet


def check_encoding(file):
    """Returns the encoding of a file"""
    with open(file, 'rb') as f:
        result = chardet.detect(f.read())
    return print(result['encoding'])
