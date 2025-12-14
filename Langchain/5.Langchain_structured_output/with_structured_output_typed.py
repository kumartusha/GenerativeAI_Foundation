from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from typing import TypedDict
from langchain_groq import ChatGroq
import os

load_dotenv()

# model = ChatOpenAI(model="gpt-4.1-2025-04-14")
model = ChatGroq(model="openai/gpt-oss-120b", api_key=os.getenv("GROK_API_KEY"))

# Schema of the Data
class Review(TypedDict):

    summary: str
    sentiment: str
    product_information: str

structured_model = model.with_structured_output(Review)

result = structured_model.invoke("""The hardware is great, but the software feels bloated. There are too many pre-installed apps that I can't remove. Also, the UI looks outdated compared to other brands. Hoping for a software update to fix this.""")

print(result)