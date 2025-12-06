from langchain_core.messages import SystemMessage, HumanMessage,AIMessage
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

model = ChatGroq(model="openai/gpt-oss-120b", api_key=os.getenv("GROK_API_KEY"))

messages = [
    SystemMessage(content="You are a helpful Assistant"),
    HumanMessage(content="How to be the better person"),
]

result = model.invoke(messages)

messages.append(AIMessage(content=result.content))

print(messages)