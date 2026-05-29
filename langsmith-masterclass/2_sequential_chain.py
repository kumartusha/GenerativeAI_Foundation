from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

# Overwrite the .env project name.
os.environ['LANGCHAIN_PROJECT'] = "Sequential LLM App"

load_dotenv()

prompt1 = PromptTemplate(
    template='Generate a detailed report on {topic}',
    input_variables=['topic']
)

prompt2 = PromptTemplate(
    template='Generate a 5 pointer summary from the following text \n {text}',
    input_variables=['text']
)

model1 = ChatOpenAI(model="gpt-4o-mini")
model2 = ChatOpenAI(model="gpt-4o")

parser = StrOutputParser()

chain = prompt1 | model1 | parser | prompt2 | model2 | parser

config = {
    # Used for change the trace name.
    # 'run_name': 'sequential chain',
    'tags': ['llm app', 'report generation', 'summarization'],
    'metadata': {'model1': 'gpt-4o-mini', 'model1_temp': 0.7, 'parser': 'stroutputparser'}
}

# Add the dummy config
result = chain.invoke({'topic': 'Unemployment in India'}, config=config)

print(result)
