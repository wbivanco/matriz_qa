import pandas as pd 


def convert_xlsx_to_csv(file, sheet_name, csv_name, row1, row2, col1, col2):
    """Convertir un archivo excel a csv"""
    df = pd.read_excel(file, sheet_name=sheet_name)

    subset1 = df.iloc[row1:row2]

    subset2 = subset1[[col1, col2]]

    subset3 = subset2.rename(columns={col1: 'caso de prueba', col2: 'resultado esperado'})

    subset3.to_csv(csv_name, index=False, encoding='utf-8')