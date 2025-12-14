from langchain_huggingface import HuggingFaceEndpoint
from langchain_huggingface import ChatHuggingFace
from dotenv import load_dotenv
import os
from langchain_core.output_parsers import JsonOutputParser, CommaSeparatedListOutputParser, StrOutputParser, ListOutputParser, PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
import os

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    # repo_id="openai/gpt-oss-120b",
    # repo_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    task="conversational",   # ✅ must match model’s supported task
    huggingfacehub_api_token=os.getenv("HUGGING_FACE_TOKEN")
)

# model = ChatHuggingFace(llm=llm)
model = ChatGroq(model="openai/gpt-oss-120b", api_key=os.getenv("GROK_API_KEY"))

# parser = JsonOutputParser()
parser = CommaSeparatedListOutputParser()

template = PromptTemplate(
    template="Give me 5 facts about {topic} \n {format_instruction}",
    # template="Give me 5 facts about {topic}",
    input_variables=["topic"],
    # it will add the Return a Json Object in the prompt instead of the format_instruction.
    partial_variables={'format_instruction': parser.get_format_instructions()}
)

# Instead of these three lines we can use the chain concept.
# prompt = template.format()
# result = model.invoke(prompt)
# final_result = parser.parse(result.content)


chain = template | model | parser
result = chain.invoke({"topic": "HFT Trading"})

print(result)