import chardet

""" Modo de uso:
from libs.check_encoding import check_encoding

check_encoding('ruta_al_archivo.xlsx')
"""


def check_encoding(file):
    """Returns the encoding of a file"""
    
    if file is None:    
        raise ValueError('Debe enviar un archivo válido')
    
    with open(file, 'rb') as f:
        result = chardet.detect(f.read())
    return print(result['encoding'])
