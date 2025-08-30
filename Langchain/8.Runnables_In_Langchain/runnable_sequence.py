# Here we will be implement the Simple Chain in the langchain with the help of the Chains.
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence

load_dotenv()

# we initialize the model.
model = ChatOpenAI(model="gpt-4o-mini")

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

# First Method
# chain = template | model | parser

# result = chain.invoke({'topic': 'HFT Trading'})

# Second Method.