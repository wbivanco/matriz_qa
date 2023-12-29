import chardet
import tiktoken

""" Modo de uso -> check_encoding:
from libs.check_encoding import check_encoding

check_encoding('ruta_al_archivo.xlsx')
"""


def check_file_encoding(file):
    """Returns the encoding of a file"""
    
    if file is None:    
        raise ValueError('Debe enviar un archivo válido')
    
    with open(file, 'rb') as f:
        result = chardet.detect(f.read())

    return print(result['encoding'])


def number_tokens(model, text=''):
    """Return the number of tokens in a string."""

    if model is None:    
        raise ValueError('Debe enviar un modelo ')
    
    encoding = tiktoken.encoding_for_model(model)

    return len(encoding.encode(text))