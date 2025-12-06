# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.messages import HumanMessage, SystemMessage


# chat_prompt_template = ChatPromptTemplate([
#     ('system', 'You are a helpful {domain} expert'),
#     ('human', 'Explain in simple term what is {topic}')
# ])


# prompt = chat_prompt_template.invoke({'domain': 'finance', 'topic': 'Trading'})

# print(prompt)


from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

model = ChatGroq(model="openai/gpt-oss-120b", api_key=os.getenv("GROK_API_KEY"))

chat_prompt_template = ChatPromptTemplate([
    SystemMessage(content="""
        You are the finance expext that explain the complex things in the simple way.
        If you dont know the answer simply say that I don't Know.
                 
        Context : {context}
        chat_history: {chat_history}"""),
    HumanMessage(content="{question}"),
])

prompt = chat_prompt_template.format_messages(
    context="Only give the answer from the relevent resource.",
    chat_history="User: Hi \n Assistant: Hello",
    question="who is the prime minister of the india"
)