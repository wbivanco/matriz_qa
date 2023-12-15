import docx
import re
import csv

def getText(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)

def getDoc(filename):
    text=getText(filename)
    textmod=re.sub(r'\n+', '\n', text)
    return textmod

def getCsv(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        csv_content = '\n'.join(','.join(row) for row in reader)
    return csv_content    
