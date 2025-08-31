# Here we will be implement the Simple Chain in the langchain with the help of the Chains.

from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# we initialize the model.
model = ChatOpenAI(model="gpt-4o-mini")

# we initialize the parser.
parser = StrOutputParser()

# Initialize the template
template = PromptTemplate(
    template="Give me 6 line of poem on {topic}",
    input_variables=['topic']
)

# Build the simple chain (Pipeline)

chain = template | model | parser

result = chain.invoke({'topic': 'HFT Trading'})

print(result)

chain.get_graph().print_ascii()