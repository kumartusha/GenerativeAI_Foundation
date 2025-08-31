from langchain_huggingface import HuggingFaceEndpoint
from langchain_huggingface import ChatHuggingFace
from dotenv import load_dotenv
import os
from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    # repo_id="openai/gpt-oss-120b",
    # repo_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    task="conversational",   # ✅ must match model’s supported task
    huggingfacehub_api_token=os.getenv("HUGGING_FACE_TOKEN")
)

model = ChatHuggingFace(llm=llm)

# Build the Schema for the structured output Parser.
schema = [
    ResponseSchema(name="fact_1", description="Fact 1 about the topic"),
    ResponseSchema(name="fact_2", description="Fact 2 about the topic"),
    ResponseSchema(name="fact_3", description="Fact 3 about the topic")
]


parser = StructuredOutputParser.from_response_schemas(schema)

template = PromptTemplate(
    template="Give 4 facts about the {topic} \n {format_instructions}",
    input_variables=['topic'],
    partial_variables={'format_instructions': parser.get_format_instructions()}
)

# Without Chain
# prompt = template.invoke({'topic': "HFT Trading"})
# result = model.invoke(prompt)
# final_result = parser.parse(result.content)


# With Chain
chain = template | model | parser
result = chain.invoke({'topic': "HFT Trading"})

print(result)
