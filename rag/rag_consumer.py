from icecream import ic
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from dotenv import load_dotenv
from pathlib import Path

# Cargar variables de entorno desde .env
load_dotenv()




# Inicializar el modelo de embeddings y el modelo de lenguaje
embeddings_model = OpenAIEmbeddings()
llm = ChatOpenAI(model="gpt-4o-mini-2024-07-18", temperature=0)

# Cargar el índice FAISS desde el disco
ic("Cargando índice FAISS...")
script_path = Path(__file__).resolve()
faiss_index_path = str(script_path.parent / "faiss_index")
ic(faiss_index_path)
index = FAISS.load_local(faiss_index_path, embeddings=embeddings_model, allow_dangerous_deserialization=True)


def consulta_modelo(query_user, contexto=None):
    mensajes = [
        {"role": "system", "content": f"""
                Eres un asistente util, para educar a las personas de El Salvador sobre la ley de los consumidores
                que existe el pais.
                
                
                Se te brindara contexto, para que des respuesta al usuario.
                Modelos posibles:{contexto}
                        
                        
                Instruccion **ESTRICTA**:                        
                Pero si el contexto esta vacio y tu conoces la respuesta, responder pero en posdata indica que
                el conocimiento no esta basado en la ley directamente escrita en El Salvador.

            """},
        {"role": "user", "content": f"Consulta de usuario: {query_user}"}
    ]

    respuesta = llm.invoke(mensajes)
    return respuesta.content


# Función para realizar una consulta al sistema RAG
def consultar_rag(query, k=5):
    ic("consultar_rag")

    # Recuperar los documentos más relevantes del índice FAISS
    resultados = index.similarity_search(query, k=k)

    # Extraer el contenido de los documentos recuperados
    contexto = "\n\n".join([
        f"""                            
            {resultado.page_content}            
        """
        for resultado in resultados])

    return  contexto


def logical_progression(query_user):
    contexto = consultar_rag(query_user, 5)
    respuesta = consulta_modelo(query_user, contexto)
    return respuesta


# Ejemplo de uso del sistema RAG
if __name__ == "__main__":
    consulta = """
    Segun la ley de el salvador, cuales son los derechos basicos de los consumidores?    
    """
    res = logical_progression(consulta)
    print(res)