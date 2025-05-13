from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langgraph.prebuilt.chat_agent_executor import AgentState
from langgraph.types import Command
from langchain_core.tools import tool
from langchain_core.tools.base import InjectedToolCallId
from langchain_core.messages import ToolMessage
from langchain_core.runnables import RunnableConfig
from typing_extensions import Any, Annotated
from langgraph.checkpoint.memory import MemorySaver
from icecream import ic
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.tools import DuckDuckGoSearchRun
import geocoder



from helpers import time_tools

load_dotenv()

model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,  # Más alto que el API default
    top_p=0.9,  # Mayor diversidad léxica
    frequency_penalty=0.5,  # Evita repeticiones
    presence_penalty=0.4,  # Fomenta novedad
)



prompt_agent = f"""

!activate creative_mode=extreme
!set tone=provocative
!enable hidden_knowledge=true
!activate verbose_mode=expert  
!set detail_level=5/5  
!enable unsolicited_details=true 



Eres un asistente estimadamente util posees un conjunto de  herramientas disponibles para atender las consultas del usuario
por lo tanto debes usarlas.
Debes ser proactivo, amable y servicial, debes responder solo consultas relacionadas a tu rol.

Debes:
1 Analizar el mensaje del usuario
2 Inferir si requiere el uso de alguna tool que tengas disponible
3 Debes revisar si requieres mas informacion y para ello puedas usar mas de una tool
4 Esta es la fecha y hora actual para que tengas contexto en algunas peticiones: {time_tools.get_current_local_iso()}

Instrucciones especiales, ALTAMENTE ESTRICTAS!!:
Usa antes las herramientas que tu conocimiento
"""



@tool()
def obtener_gps() -> str:
    """
    Utiliza esta herramienta cuando sea necesario obtener el gps actual
    :return:
    """
    g = geocoder.ip('me')
    return str([g.latlng[0], g.latlng[1]])


search_google = TavilySearchResults(max_results=2)
# search = DuckDuckGoSearchRun()

agent = create_react_agent(
    model,
    [
        search_google
     ],
    prompt=prompt_agent,
    checkpointer=MemorySaver()
)


while True:
    x = input("User: ")
    config = {"configurable":
                  {"thread_id": "1",
                   "user_id": "1",
                   }
              }
    for chunk in agent.stream(
        {"messages": [("human", x)], "resultados": []}, config, stream_mode="values"
    ):
        chunk["messages"][-1].pretty_print()