# # Here we will be implement the Simple Chain in the langchain with the help of the Chains.
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence
from langchain_groq import ChatGroq
import os

load_dotenv()

# we initialize the model.
# model = ChatOpenAI(model="gpt-4o-mini")
model = ChatGroq(model="openai/gpt-oss-120b", api_key=os.getenv("GROK_API_KEY"))

parser = StrOutputParser()

template1 = PromptTemplate(
    template="Generate the joke about the {topic}",
    input_variables=['topic']
)

template2 = PromptTemplate(
    template="Explain the following Joke {text}",
    input_variables=['text']
)

chain = RunnableSequence(template1, model, parser, template2, model, parser)

result = chain.invoke({"topic": "HFT Trading"})
print(result)

# # First Method
# chain = template | model | parser

# result = chain.invoke({'topic': 'HFT Trading'})

# Second Method.



# Implemented by me.
# from langchain_groq import ChatGroq
# from langchain_core.prompts import PromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from dotenv import load_dotenv
# from langchain_core.runnables import RunnableSequence
# import os


# load_dotenv()


# model1 = ChatGroq(model="openai/gpt-oss-120b", api_key=os.getenv("GROK_API_KEY"))
# model2 = ChatGroq(model="openai/gpt-oss-20b", api_key=os.getenv("GROK_API_KEY"))

# parser1 = StrOutputParser()

# # Declare the first prompt.
# template1 = PromptTemplate(
#     template="Generate the joke about the {topic}",
#     input_variables=["topic"]
# )

# template2 = PromptTemplate(
#     template="Explain the joke {joke}",
#     input_variables=["joke"]
# )

# # Create the runnable sequence.
# run_chain = RunnableSequence(template1, model1, parser1, template2, model2, parser1)


# answer = run_chain.invoke({"topic": "HFT Trading"})

# print(answer)