from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field
from langchain_core.runnables import RunnableBranch, RunnableLambda
from typing import Literal, Annotated
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize the Pydantic Class.
class Sentiment(BaseModel):
    sentiment: Literal["Positive", "Negative", "Neutral"] = Field(description="This is used for the sentiment")

# Initialize the Model.
model = ChatGroq(model="openai/gpt-oss-120b", api_key=os.getenv("GROK_API_KEY"))

# Initialize the Parser.
parser1 = PydanticOutputParser(pydantic_object=Sentiment)
parser2 = StrOutputParser()

# Initialize the prompt 1.

template1 = PromptTemplate(
    template="Generate the positive or negative sentiment based on the {text}. \n {format_instruction}",
    input_variables=["text"],
    partial_variables={"format_instruction": parser1.get_format_instructions()}
)

chain = template1 | model | parser1

# Initialize the conditional Chain.
template2 = PromptTemplate(
    template="Write an appropriate response to this positive feedback {text}",
    input_variables=["text"]
)

template3 = PromptTemplate(
    template="Write an appropriate response to this negative feedback {text}",
    input_variables=["text"]
)

# Initialize the Conditional Chain.
conditional_chain = RunnableBranch(
    (lambda x:x.sentiment == "Positive", template2 | model | parser2),
    (lambda x:x.sentiment == "Negative", template3 | model | parser2),
    RunnableLambda(lambda x: "Could not find the sentiment")
)

final_chain = chain | conditional_chain

answer = final_chain.invoke({"text": "My name is tushar and its amazing experience so far."})
print(answer)

# final_chain.get_graph().print_ascii()