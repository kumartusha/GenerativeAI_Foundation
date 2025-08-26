from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

embedding = OpenAIEmbeddings(model="text-embedding-3-large", dimensions=3072)

result = embedding.embed_query("Delhi is the capital of india ??")
print(result)

print(len(result))