# from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
# from dotenv import load_dotenv
# import os
# from langchain_core.prompts import PromptTemplate
# from langchain_core.output_parsers import PydanticOutputParser
# from pydantic import BaseModel, Field
# from langchain_groq import ChatGroq

# load_dotenv()

# llm = HuggingFaceEndpoint(
#     repo_id="meta-llama/Llama-3.1-8B-Instruct",
#     # repo_id="openai/gpt-oss-120b",
#     # repo_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
#     task="conversational",   # ✅ must match model’s supported task
#     huggingfacehub_api_token=os.getenv("HUGGING_FACE_TOKEN")
# )

# # model = ChatHuggingFace(llm=llm)
# model = ChatGroq(model="openai/gpt-oss-120b", api_key=os.getenv("GROK_API_KEY"))

# class Person(BaseModel):
#     name: str = Field(description="Name of the person")
#     age: int = Field(gt=18, lt=99,description="Age of the person")
#     city: str = Field(description="Name of the city the person belongs to")


# parser = PydanticOutputParser(pydantic_object=Person)

# template = PromptTemplate(
#     template="Generate the name, age and city of a fictional {place} person \n {format_instruction}",
#     input_variables=['place'],
#     partial_variables={'format_instruction': parser.get_format_instructions()}
# )

# # Without using the chain.
# # prompt = template.invoke({'place': "indian"})

# # # print(prompt)

# # result = model.invoke(prompt)

# # final_result = parser.parse(result.content)


# # Create the chain.
# chain = template | model | parser

# final_result = chain.invoke({'place': 'indian'})

# print(final_result)



from langchain_groq import ChatGroq
from langchain_core.output_parsers import CommaSeparatedListOutputParser, StrOutputParser, PydanticOutputParser
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Optional, Annotated

load_dotenv()

class Vehicle(BaseModel):
    make: str = Field(description="This is the vehicle name of the provided brand")
    model : str = Field(description="This is the age of the vehicle")
    variant: str = Field(description="This is the variant name of the vehicle")
    reg_year: int = Field(gt=2021, lt=2025, description="Registration number of the vehicle")
    state: str = Field(description="ABout the any state name.")
    engine_capacity: str = Field(description="About the vehicle capacity")
    ownership: int = Field(gt=0, lt=3, description="This is about the ownership of the vehicle.")
    fuel_tank: int = Field(gt=70, lt=300, description="This is about the vehicle tank with Litre unit.")
    

model = ChatGroq(model="openai/gpt-oss-120b", api_key=os.getenv("GROK_API_KEY"))

parser = PydanticOutputParser(pydantic_object=Vehicle)

# Here we do the prompt injection to get the details about the vehicle.
prompt = PromptTemplate(
    template="Give me the details about the {brand}. \n {format_instruction}",
    input_variables=["brand"],
    partial_variables={"format_instruction": parser.get_format_instructions()}
)

# Creating the chain.
chain = prompt | model | parser

answer = chain.invoke({"brand": "Mahindra"})

print(answer)