# Here we will be build the Sequential chain using the LLM.

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


load_dotenv()

prompt1 = PromptTemplate(
    template="Give me the 10 points about the {topic}",
    input_variables=['topic']
)

prompt2 = PromptTemplate(
    template="Summarize these points and give me 5 most important points. {text}",
    input_variables=['text']
)

model = ChatOpenAI(model="gpt-4o-mini")

parser = StrOutputParser()

chain = prompt1 | model | parser | prompt2 | model | parser

result = chain.invoke({'topic': 'HFT Trading'})

print(result)

chain.get_graph().print_ascii()