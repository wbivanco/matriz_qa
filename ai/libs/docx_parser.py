import docx
import re
import csv


def validate_file(filename):
    """Validates if the file is a docx or csv file and if filename is not empty"""
    if filename is None:
        raise ValueError('Debe enviar un archivo válido')

    if not filename.endswith('.docx') and not filename.endswith('.csv'):
         raise ValueError('Debe enviar un archivo con extensión .docx o .csv')
    
    return True


def getText(filename):
    """Returns the text of a docx file, with extra lines"""
    if validate_file(filename):
        doc = docx.Document(filename)
        fullText = []
        for para in doc.paragraphs:
            fullText.append(para.text)
        return '\n'.join(fullText)


def getDoc(filename):
    """Returns the text of a docx file, with no extra lines"""
    if validate_file(filename):
        text = getText(filename)
        textmod = re.sub(r'\n+', '\n', text)
        return textmod


def getCsv(filename):
    """Returns the text of a csv file, with no extra lines"""
    if validate_file(filename):
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            csv_content = '\n'.join(','.join(row) for row in reader)
        return csv_content    
