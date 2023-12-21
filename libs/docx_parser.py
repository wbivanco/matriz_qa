import docx
import re
import csv


def getText(filename):
    """Returns the text of a docx file, with extra lines"""
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)


def getDoc(filename):
    """Returns the text of a docx file, with no extra lines"""
    text=getText(filename)
    textmod=re.sub(r'\n+', '\n', text)
    return textmod


def getCsv(filename):
    """Returns the text of a csv file, with no extra lines"""
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        csv_content = '\n'.join(','.join(row) for row in reader)
    return csv_content    
