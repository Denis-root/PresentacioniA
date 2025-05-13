from icecream import ic
from helpers import tiktoken_tools
from helpers.file_tools import leer_txt
from helpers.clean_strings import limpiar_texto
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import os
import json

# Cargar las variables de entorno desde el archivo .env
load_dotenv()


# Inicializar el modelo de embeddings con OpenAI
embeddings_model = OpenAIEmbeddings()

# Crear una lista para almacenar los textos y metadatos
documentos = []
metadatos = []


from pathlib import Path
script_path = Path(__file__).resolve()
ruta = str(script_path.parent / "docs")
ic(ruta)



for archivo, contenido in leer_txt(ruta):
    print(f"Archivo: {archivo}")
    contenido_limpio = limpiar_texto(contenido)

    # Calcular el número de tokens
    tik_tokens = tiktoken_tools.contar_tokens(contenido)
    ic(f"Tokens para el documento: {tik_tokens}")

    # Agregar el texto y los metadatos a las listas
    documentos.append(contenido)
    metadatos.append({"nombre_archivo": archivo.name})


# Generar los embeddings para todos los documentos
ic("Generando embeddings...")
vectores = embeddings_model.embed_documents(documentos)

# Crear el índice FAISS con textos, embeddings y metadatos
ic("Creando índice FAISS...")
index = FAISS.from_texts(texts=documentos, embedding=embeddings_model, metadatas=metadatos)

# Guardar el índice en disco (opcional)
index.save_local("faiss_index")

ic("Índice FAISS creado y guardado exitosamente.")
