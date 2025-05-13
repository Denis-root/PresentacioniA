from icecream import ic
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from dotenv import load_dotenv


# Cargar variables de entorno desde .env
load_dotenv()


llm = ChatOpenAI(model="gpt-4o-mini-2024-07-18", temperature=0)


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


def logical_progression(query_user):
    respuesta = consulta_modelo(query_user)
    return respuesta


# Ejemplo de uso del sistema RAG
if __name__ == "__main__":
    consulta = """
    Segun la ley de el salvador, cuales son los derechos basicos de los consumidores?    
    """
    res = logical_progression(consulta)
    print(res)