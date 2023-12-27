import pandas as pd 

""" Modo de uso:
from libs.convert_excel_to_csv import convert_xlsx_to_csv

convert_xlsx_to_csv('ruta_al_archivo.xlsx', 'nombre_hoja', 'nombre_columa1', 'nombre_columa1', 'ruta_al_archivo.csv', numero_fila1, numero_fila2)
"""


def convert_xlsx_to_csv(file, sheet_name, col1, col2, csv_name='nombre_por_defecto', row1=0, row2=300):
    """Convertir un archivo excel a csv"""'Nombre de la hoja', 

    # Validaciones varias para campos obligatorios por la lógica del programa.
    if file is None:
        raise ValueError('Debe enviar un archivo válido')
    
    if sheet_name is None:
        raise ValueError('Debe enviar un nombre de hoja válido')
    
    if col1 is None and col2 is None:
        raise ValueError('Debe enviar dos nombres de columna válidos') 
    
    df = pd.read_excel(file, sheet_name=sheet_name)

    subset1 = df.iloc[row1:row2]

    subset2 = subset1[[col1, col2]]

    subset3 = subset2.rename(columns={col1: 'caso de prueba', col2: 'resultado esperado'})

    subset3.to_csv(csv_name, index=False, encoding='utf-8')