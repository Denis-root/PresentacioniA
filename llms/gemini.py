from dotenv import load_dotenv
load_dotenv()
from icecream import ic
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="models/gemini-1.5-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)

messages = [
    (
        "system",
        "Eres un asistente polimata sabes responder a todo por que sabes de todo y respondes de una manera que hasta un niño puede responder.",
    ),
    ("human", "Por que en agua hirviendo, la papa se ablanda pero los huevos se endurecen?"),
]

ai_msg = llm.invoke(messages)
ic(ai_msg.content)