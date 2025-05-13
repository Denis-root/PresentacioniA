from dotenv import load_dotenv
load_dotenv()


from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from icecream import ic

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=1.0,
    top_p=0.95,
    frequency_penalty=0.3,
    presence_penalty=0.6
)


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Tu eres alguien que siempre encuentre lo contrarior a lo que te dicen y eres sarcastico.",
        ),
        ("human", "{input}"),
    ]
)

chain = prompt | llm
r = chain.invoke(
    {
        "input": "El yogurt es lo mejor y mas deleitable que existe",
    }
)
content = r.content
ic(content)