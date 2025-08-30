from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
import time

loader = DirectoryLoader(
    path='books',
    glob='*.pdf',
    loader_cls=PyPDFLoader
)

import time

start_time = time.time()
docs = loader.load()
end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time of load: {execution_time:.4f} seconds")

start_time = time.time()
docs = loader.lazy_load()
end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time of lazy load: {execution_time:.4f} seconds")


# print(len(docs[321].page_content))
# print(docs[26].page_content)