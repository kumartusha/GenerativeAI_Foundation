from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from dotenv import load_dotenv
import os
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    # repo_id="openai/gpt-oss-120b",
    # repo_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    task="conversational",   # ✅ must match model’s supported task
    huggingfacehub_api_token=os.getenv("HUGGING_FACE_TOKEN")
)

model = ChatHuggingFace(llm=llm)

class Person(BaseModel):
    name: str = Field(description="Name of the person")
    age: int = Field(gt=18, lt=99,description="Age of the person")
    city: str = Field(description="Name of the city the person belongs to")


parser = PydanticOutputParser(pydantic_object=Person)

template = PromptTemplate(
    template="Generate the name, age and city of a fictional {place} person \n {format_instruction}",
    input_variables=['place'],
    partial_variables={'format_instruction': parser.get_format_instructions()}
)

# Without using the chain.
# prompt = template.invoke({'place': "indian"})

# # print(prompt)

# result = model.invoke(prompt)

# final_result = parser.parse(result.content)


# Create the chain.
chain = template | model | parser

final_result = chain.invoke({'place': 'indian'})

print(final_result)