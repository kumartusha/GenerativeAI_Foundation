# Langchain using the Langchain Chatmodels

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenAI(temperature=2, model="gpt-3.5-turbo", api_key=os.getenv("OPENAI_API_KEY"), max_tokens=1000)

print("=====" * 20)
print(llm.invoke("write a 5 line poem on cricket in english??").content)
 