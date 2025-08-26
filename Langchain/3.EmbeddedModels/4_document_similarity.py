from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

load_dotenv()

embedding = OpenAIEmbeddings(model="text-embedding-3-large", dimensions=300)

documents = [
    "Who is Virat Kohli and why is he considered one of the greatest batsmen in modern cricket history?",
    "What is the capital city of Japan, and why is it known as a hub of technology and culture?",
    "Who invented the telephone, and how did this invention change the way humans communicate?",
    "What is the national animal of India, and what is its cultural and environmental significance?",
    "Which planet in our solar system is called the Red Planet, and why does it have that nickname?",
    "Who is regarded as the Father of the Nation in India, and what role did he play in India’s independence?",
    "What is the largest ocean in the world, and how does it affect global climate and trade routes?",
    "Who painted the famous artwork Mona Lisa, and why is it considered one of the most iconic paintings in history?"
]

query = "which game is most popular that will initiated by the britishers ?? "

documents_embeddings = embedding.embed_documents(documents)
query_embedding = embedding.embed_query(query)


# this will give the similarity of the query with the all document in the list.
# [ 0.20332027  0.07403756 -0.01426244  0.12737352  0.0814674   0.21515
#    0.0743327   0.04174759]]
scores = cosine_similarity([query_embedding], documents_embeddings)[0]
index, score = sorted(list(enumerate(scores)), key=lambda x:x[1])[-1]

print(query)
print(documents[index])
print("Similarity score is :- ", score)