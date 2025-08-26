# 

from langchain_openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

llm = OpenAI(temperature=0.1, model="gpt-3.5-turbo-instruct", api_key=os.getenv("OPENAI_API_KEY"), max_tokens=1000)

result = llm.invoke("can you tell me about the 91trucks in details along with the suggestion should i visit on that or not ??")

print(result)