# Here we will be implement the Simple Chain in the langchain with the help of the Chains.
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence, RunnablePassthrough, RunnableParallel
from langchain.schema.runnable import RunnableLambda, RunnableBranch

load_dotenv()


prompt = PromptTemplate(
    template="Write a detailed report on {topic}",
    input_variables=['topic']
)
  
prompt2 = PromptTemplate(
    template='Summarize the following text \n {text}',
    input_variables=['text']
)
 
model = ChatOpenAI(model='gpt-4o-mini')

parser = StrOutputParser()

# report_gen_chain = RunnableSequence(prompt, model, parser)
report_gen_chain = prompt | model | parser

branch_chain = RunnableBranch(
    (lambda x: len(x.split()) > 400, RunnableSequence(prompt2, model, parser)),
    RunnablePassthrough()
)

final_chain = RunnableSequence(report_gen_chain, branch_chain)

result = final_chain.invoke({'topic': 'HFT Trading'})

print(result)