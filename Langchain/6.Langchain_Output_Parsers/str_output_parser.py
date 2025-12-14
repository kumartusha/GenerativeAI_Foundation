# from langchain_huggingface import HuggingFaceEndpoint
# from langchain_huggingface import ChatHuggingFace
# from dotenv import load_dotenv
# import os
# from langchain_core.prompts import PromptTemplate
# from langchain_groq import ChatGroq

# load_dotenv()

# llm = HuggingFaceEndpoint(
#     # repo_id="openai/gpt-oss-120b",
#     repo_id="openai/gpt-oss-120b",
#     # repo_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
#     task="conversational",   # ✅ must match model’s supported task
#     huggingfacehub_api_token=os.getenv("HUGGING_FACE_TOKEN")
# )

# # model = ChatHuggingFace(llm=llm)
# model = ChatGroq(model="openai/gpt-oss-120b", api_key=os.getenv("GROK_API_KEY"))

# # 1st prompt -> Detailed Report
# template1 = PromptTemplate(
#     template="Write a detailed report on {topic}",
#     input_variables=['topic']
# )

# prompt1 = template1.invoke({'topic': 'HFT Trading'})

# result = model.invoke(prompt1)

# # 2nd prompt -> Summary
# template2 = PromptTemplate(
#     template="write a 5 line summary on the following text. /n {text}",
#     input_variables=['text']
# )
# prompt2 = template2.invoke({'text': result.content})

# result2 = model.invoke(prompt2)

# print(result2.content)

# Implementation by Me.

from langchain_groq import ChatGroq
from langchain_core.output_parsers import CommaSeparatedListOutputParser, StrOutputParser, PydanticOutputParser
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

# Initialized the Models.
model1 = ChatGroq(model="openai/gpt-oss-120b", api_key=os.getenv("GROK_API_KEY"))
model2 = ChatGroq(model="openai/gpt-oss-20b", api_key=os.getenv("GROK_API_KEY"))

# Initialized the Parsers.
parser1 = StrOutputParser()
parser2 = CommaSeparatedListOutputParser()

# Initialized the Prompt.
template1 = PromptTemplate(
    template="Give me the detailed report about the {topic}.",
    input_variables=["topic"],
    # partial_variables={"format_instruction": parser1.get_format_instructions()}
)

# prompt = template1.invoke({"topic": "HFT Trading"})

# result1 = model1.invoke(prompt)

# print(result1.content)

chain1 = template1 | model1 | parser1

# result1 = chain1.invoke({"topic": "HFT Trading"})

# Initialized the Prompt 2 for summarizing the content.
template2 = PromptTemplate(
    template="Summarize this entire report into the 5 bullet points. \n {story}.",
    input_variables=["story"],
    # partial_variables={"format_instruction": parser2.get_format_instructions()}
)

# chain2 = prompt2 | model2 | parser2

# prompt2 = template2.invoke({"story": result1.content})

# result2 = model2.invoke(prompt2)

chain2 = template2 | model2 | parser2

result2 = chain2.invoke({"story": chain1.invoke({"topic": "HFT Trading"})})

print(result2)