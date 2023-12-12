from dotenv import load_dotenv
from langchain.document_loaders import UnstructuredWordDocumentLoader

from langchain.chat_models import AzureChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains.question_answering import load_qa_chain
import openai
import os


# Cargo variables de configuración
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv('API_KEY')
openai.api_type = os.getenv('API_TYPE')
openai.api_version = os.getenv('API_VERSION')
openai.api_base = os.getenv('API_BASE') # endpoint
openai.api_key = os.getenv('API_KEY')

#%%
# Chunks inferidos según el ordenamiento de texto crudo
#loader = UnstructuredWordDocumentLoader("documentos\\CP_Migraciones.docx", mode="elements")

#%%
# Texto completo
loader = UnstructuredWordDocumentLoader("documentos\\CP_Migraciones.docx")

#%%
data = loader.load()

#%%
llm = AzureChatOpenAI (
        azure_endpoint=os.getenv('API_BASE'),
        openai_api_version=os.getenv('API_VERSION'),
        deployment_name=os.getenv('CHAT_ENGINE_16K'),
        openai_api_key= os.getenv('API_KEY'),
        openai_api_type= os.getenv('API_TYPE'),
        temperature=0,
        model_version="0613" # es importante aclararlo para el correcto calculo de los costos
        )

#%%
chain = load_qa_chain(llm=llm)

#%%
query = 'cual es el resultado esperado para la prueba Prueba de funcionamiento del switch de migraciones - Desactivado'
# query = 'cual es el tema principal'
# query = 'cuales son los distintos casos de prueba'
# query = 'cuales son los distintos casos de prueba? Primero asígnale un título a cada uno, luego piensa y analiza los casos porque pueden tener subdivisiones en más casos de prueba, asígnale un segmento que puede ser prepago o pospago, finalmente enumeralos.'
response = chain.run(input_documents=data, question=query)
print(response)

# %%
prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

{context}

Question: {question}
Helpful Answer:"""

from langchain.chains.prompt_selector import ConditionalPromptSelector, is_chat_model
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)

PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)

system_template = """Use the following pieces of context to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
----------------
{context}"""

messages = [
    SystemMessagePromptTemplate.from_template(system_template),
    HumanMessagePromptTemplate.from_template("{question}"),
]

CHAT_PROMPT = ChatPromptTemplate.from_messages(messages)

PROMPT_SELECTOR = ConditionalPromptSelector(
    default_prompt=PROMPT, conditionals=[(is_chat_model, CHAT_PROMPT)]
)

chain = load_qa_chain(llm, chain_type="stuff", prompt=PROMPT_SELECTOR.get_prompt(llm))

