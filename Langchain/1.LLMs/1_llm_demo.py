# # 

# from langchain_openai import OpenAI
# from dotenv import load_dotenv
# import os

# load_dotenv()

# llm = OpenAI(temperature=0.1, model="gpt-3.5-turbo-instruct", api_key=os.getenv("OPENAI_API_KEY"), max_tokens=1000)

# result = llm.invoke("can you tell me about the 91trucks in details along with the suggestion should i visit on that or not ??")

# print(result)


# Using the Grok Model.
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()


model = ChatGroq(model="openai/gpt-oss-120b", temperature=0.2, api_key=os.getenv("GROK_API_KEY"))


result = model.invoke("Who is the prime minister of india ??")

print(result.content)