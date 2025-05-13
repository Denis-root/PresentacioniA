"""
Plantilla funcional de agente ReAct
Con langraph + herramientas
"""

from dotenv import load_dotenv
load_dotenv()
from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver


model_with_tools = ChatOpenAI(
    # model="gpt-4o-mini-2024-07-18",
    model="o3-mini-2025-01-31",
    # model="o1-mini-2024-09-12",
    # temperature=0.9,
    # top_p=0.9,
    # frequency_penalty=2.0,
    # presence_penalty=2.0,
    # n=3
)


def call_model(state: MessagesState):
    messages = state["messages"]
    response = model_with_tools.invoke(messages)
    return {"messages": [response]}


workflow = StateGraph(MessagesState)

# Define the two nodes we will cycle between
workflow.add_node("agent", call_model)


workflow.add_edge(START, "agent")
workflow.add_edge("agent", END)


# app = workflow.compile()
app = workflow.compile(checkpointer=MemorySaver())


while True:
    question = input("User: ")
    config = {"configurable":
                  {"thread_id": "1"}
              }
    for chunk in app.stream(
            {"messages": [("human", question)]}, config, stream_mode="values"
    ):
        chunk["messages"][-1].pretty_print()