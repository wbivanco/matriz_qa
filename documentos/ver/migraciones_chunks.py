# %%
##############################
import os
from os.path import abspath, dirname
from os import chdir
import sys
import docx
import re
import tiktoken
import openai
import pandas as pd
from tqdm import tqdm
import json

from configs import (
    API_TYPE,
    API_BASE,
    API_KEY,
    API_VERSION,
    CHAT_ENGINE_16K,
    GPT_MODEL,
)

# Configuracion
os.environ["OPENAI_API_KEY"] = API_KEY
openai.api_type = API_TYPE
openai.api_version = API_VERSION
openai.api_base = API_BASE # endpoint
openai.api_key = API_KEY

#%%
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

def num_tokens(text: str, model: str = GPT_MODEL) -> int:
    """Return the number of tokens in a string."""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))


#%%
path = dirname(dirname(dirname(abspath(__file__))))+'\\1.4 Datos\CP_Migraciones.docx'
# path = 'C:\\Users\\cmanoni\\OneDrive - Practia\\NLP\\4- Proyectos investigación\\NLP-Investigacion\\21. Matriz de casos de prueba - Testing+IA\\1.1 Código\\Lea\\CasoMigraciones/CP_Migraciones.docx'
docx_migraciones=getDoc(path)


#%%
def extraccion(messages, engine= CHAT_ENGINE_16K, temperature=0.1, top_p = 0.9): #top_p: da la primera mejor respuesta   

    messages_full = [{"role": "system", "content": """Sos parte del equipo de testing de una compania de telecomunicaciones.
    - Vas a recibir un documento con los requerimientos para testeo de varios de los modulos de una aplicacion y debes identificar TODOS los casos de prueba presentes en él y su resultado esperado.
    """
    }] + messages
    # y el modulo de la aplicacion al que hace alución. 
    timeout = 10
    try:
        # Hacer la solicitud a GPT
        response = openai.ChatCompletion.create(
            engine=engine,
            messages=messages_full,
            temperature=temperature,
            top_p=top_p,
            timeout=timeout
        )
    except openai.OpenAIError as e:
        print("Error al realizar la solicitud:", str(e))
        return None

    #time.sleep(1)  # Esperar un segundo antes de la próxima ejecución
    
    choice = response.choices[0]
    message = choice.get("message")
    if message is not None:
        content = message.get("content")
        if content is not None:
            return content

    print("La respuesta no contiene la clave 'content'")
    return None


def armar_mensaje(contexto, visita):
    prompt= f"""Te voy a dar un contexto y un documento, en base al documento: 
    - Identifica y enumeras TODOS los casos de prueba de testing de aplicaciones presentes (escritos) y su resultado esperado. Un ejemplo de caso de prueba es 'Validar que al darle clic en la opcion pasate un plan nos mande al la pantalla de "Pasate a un plan"' y su resultado esperado es 'Se debe mostrar la pantalla de "Pasate a un plan"'. Otro ejemplo de caso de prueba es 'Validar que al seleccionar el botón continuar permita avanzar a la pantalla de  check out' y su resultado esperado es 'Se debe mostrar la pantalla de check out'.
    - Identifica el tipo de componente de la aplicación al que hace referencia el caso de prueba (por ejemplo: 'botón continuar', 'pantalla', 'botón pasarme a un plan', 'Inicio de sesión', 'switch flujo de migraciones', 'parrillas', 'menú hamburguesa', 'campo RFC', 'Banner', 'Spinner', 'checkout', 'check box') y coloca este resultado en el campo 'componente'. 
    - Ten en cuenta que el componente tiene como máximo 5 palabras para ubicar la sección de la app, encambio el caso de prueba contiene una descripción más larga de la acción que hay que realizar.
    - Haz distinción de los casos que hablan del mantenedor y los que hablan de la app del usuario, coloca este resultado en el campo 'tipo'.
    - Además, debes identificar la funcionalidad global a la que hace referencia el texto completo, esta se encuentra generalmente al comienzo del documento. Por ejemplo: 'MANTENEDOR – SWITCH FLUJO DE MIGRACIONES-DESACTIVADO', 'MANTENEDOR – CONFIGURACIÓN DE PARRILLAS - SWITCH MOSTRAR EN EL APP – PLAN 2 – DESACTIVADO', 'MIGRACIONES – FILTRO / RANGO DE FECHAS' o descripciones similares. Este valor debes repetirlo para todos los casos de prueba que se encuentren en el documento y almacenarlo en el campo 'funcionalidad'. La funcionalidad ES IGUAL para todos los casos de prueba de un mismo documento, ignora la separación de mantenedor y app para el campo funcionalidad.
    - La salida debe ser SOLAMENTE un JSON con la informacion encontrada en el texto siguiendo la estructura: 
    {{ "1": {{
    "funcionalidad": extrae la funcionalidad y colocala aqui,
    "tipo": "mantenedor" o "aplicación",
    "componente": extrae el componente y colocalo aqui,
    "caso de prueba": extrae el caso de prueba y colocalo aqui,
    "resultado esperado": extrae el resultado esperado del caso de prueba y colocalo aqui,
  }},
  "2": {{
    "funcionalidad": extrae la funcionalidad y colocala aqui,
    "tipo": "mantenedor" o "aplicación",
    "componente": extrae el componente y colocalo aqui,
    "caso de prueba": extrae el caso de prueba y colocalo aqui,
    "resultado esperado": extrae el resultado esperado del caso de prueba y colocalo aqui,
  }},}}
    - La salida debe ser un JSON que se pueda leer mediante json.loads() en python, incluye siempre los separadores correspondientes para que funcione la lectura. 
    Contexto: {contexto}
    Documento:{visita}"""
    mensaje= [{"role": "user", "content": prompt}]
    return extraccion(mensaje)


#%%
# Separa cada título del docx en un chunk:
# reemplazar '.\n-' por '#' para identificar cada título.
# separar texto en chunks por caracter '#'. 
docx_migraciones_md = docx_migraciones.replace('.\n-', '#')
docx_migraciones_md = docx_migraciones_md.replace('\n–', '#')
chunks_md = docx_migraciones_md.split('#')
contexto = chunks_md[0]
documentos = chunks_md[1:]


#%%
### bloque de codigo para almacenar en un DataFrame los resultados de todos los chunks
# Inicializa un DataFrame vacío con las columnas deseadas
resultados = pd.DataFrame(columns=['funcionalidad','tipo','componente','caso de prueba', 'resultado esperado'])

# Itera sobre cada chunk en 'documentos'
for chunk in tqdm(documentos):
    # Llama a `armar_mensaje` con el chunk como argumento
    casos_de_prueba = armar_mensaje(contexto,chunk)
    
    # Convierte la cadena de texto en un diccionario
    casos_de_prueba_dict = json.loads(casos_de_prueba)
    
    # Convierte el diccionario anidado en un DataFrame y añádelo al DataFrame de resultados
    for key, value in casos_de_prueba_dict.items():
        df = pd.DataFrame(value, index=[0])
        resultados = pd.concat([resultados, df], ignore_index=True)

# Ahora 'resultados' es un DataFrame que contiene todos los casos de prueba de todos los chunks


#%%
# Guarda los resultados en un archivo CSV que se lean ñ y tildes
resultados.to_csv('resultados.csv', index=False, encoding='utf-8-sig')
