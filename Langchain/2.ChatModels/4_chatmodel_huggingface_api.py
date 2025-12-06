from langchain_huggingface import HuggingFaceEndpoint
from langchain_huggingface import ChatHuggingFace
from dotenv import load_dotenv
import os

load_dotenv()

llm = HuggingFaceEndpoint(
    # repo_id="openai/gpt-oss-120b",
    repo_id="meta-llama/Llama-3.2-1B-Instruct",
    # repo_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    task="conversational",   # ✅ must match model’s supported task
    huggingfacehub_api_token=os.getenv("HUGGING_FACE_TOKEN"),
)

model = ChatHuggingFace(llm=llm)

print(model.invoke("How to become the billionare in the trading market ??").content)