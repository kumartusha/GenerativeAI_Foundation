from langchain_huggingface import HuggingFaceEndpoint
from langchain_huggingface import ChatHuggingFace
from dotenv import load_dotenv
import os
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

load_dotenv()

llm = HuggingFaceEndpoint(
    # repo_id="openai/gpt-oss-120b",
    repo_id="openai/gpt-oss-120b",
    # repo_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    task="conversational",   # ✅ must match model’s supported task
    huggingfacehub_api_token=os.getenv("HUGGING_FACE_TOKEN")
)

model = ChatHuggingFace(llm=llm)

# 1st prompt -> Detailed Report
template1 = PromptTemplate(
    template="Write a detailed report on {topic}",
    input_variables=['topic']
)

prompt1 = template1.invoke({'topic': 'HFT Trading'})

result = model.invoke(prompt1)

# 2nd prompt -> Summary
template2 = PromptTemplate(
    template="write a 5 line summary on the following text. /n {text}",
    input_variables=['text']
)

parser = StrOutputParser()

# Pipeline using the parser from left to right. (Parsers remove the irrelevent data like metadata )
chain = template1 | model | parser | template2 | model | parser
result = chain.invoke({'topic': "HFT Trading"})
print(result)