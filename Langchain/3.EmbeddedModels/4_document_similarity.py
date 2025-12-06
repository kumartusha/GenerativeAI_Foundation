# from langchain_openai import OpenAIEmbeddings
# from dotenv import load_dotenv
# from sklearn.metrics.pairwise import cosine_similarity
# from langchain_huggingface import HuggingFaceEmbeddings
# import numpy as np

# load_dotenv()

# # embedding = OpenAIEmbeddings(model="text-embedding-3-large", dimensions=300)
# embedding = HuggingFaceEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2")

# documents = [
#     "Who is Virat Kohli and why is he considered one of the greatest batsmen in modern cricket history?",
#     "What is the capital city of Japan, and why is it known as a hub of technology and culture?",
#     "Who invented the telephone, and how did this invention change the way humans communicate?",
#     "What is the national animal of India, and what is its cultural and environmental significance?",
#     "Britishers are always into the panic mode from the indians."
#     "Which planet in our solar system is called the Red Planet, and why does it have that nickname?",
#     "Who is regarded as the Father of the Nation in India, and what role did he play in India’s independence?",
#     "What is the largest ocean in the world, and how does it affect global climate and trade routes?",
#     "Who painted the famous artwork Mona Lisa, and why is it considered one of the most iconic paintings in history?"
# ]

# query = "which game is most popular that will initiated by the britishers ?? "

# documents_embeddings = embedding.embed_documents(documents)
# query_embedding = embedding.embed_query(query)

# print(documents_embeddings)
# print(query_embedding)

# # this will give the similarity of the query with the all document in the list.
# # [ 0.20332027  0.07403756 -0.01426244  0.12737352  0.0814674   0.21515
# #    0.0743327   0.04174759]]
# scores = cosine_similarity([query_embedding], documents_embeddings)[0]
# index, score = sorted(list(enumerate(scores)), key=lambda x:x[1])[-1]

# print(query)
# print(documents[index])
# print("Similarity score is :- ", score)



# we need to build the semantic search tool.
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np



embeddings = HuggingFaceEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2")

documents= [
    "Tree is used to provide the oxygen for the living things",
    "Virat kohli is one of the most follower and the richest cricketer in india",
    "Hugging face is the open source community that will be helpful for the developers who need the pretrained model.",
    "AI-ML Engineer work on the both side that in the data science and the development side.",
    "HTML is the Hyper text programming language but the java is used for building the scalable Backend.",
    "There are types of problem into the machine learning like the supervised, unsupervised, overfitting, underfitting"
]

query = "Virat kohli is one of the most follower and the richest cricketer in india"

query_embedding = embeddings.embed_query(query)
document_embedding = embeddings.embed_documents(documents)

# my_query_embedding = np.array(query_embedding)
# reshaped_array = my_query_embedding.reshape(-1,1)

scores = cosine_similarity([query_embedding], document_embedding)
print(scores)