from langchain_community.document_loaders import TextLoader
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(model='gpt-4o-mini')

prompt = PromptTemplate(
    template='write a summary for the following poem {poem}',
    input_variables=['poem']
)

parser = StrOutputParser()

loader = TextLoader(file_path="cricket.txt", encoding='utf-8')

docs = loader.load()

# print("=====" * 20)
# print(docs[0].page_content)
# print(docs[0].metadata)
# print(type(docs))
# print("=====" * 20)

chain = prompt | model | parser

print(chain.invoke({'poem': docs[0].page_content}))