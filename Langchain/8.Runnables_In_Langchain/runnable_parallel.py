# Here we will be implement the Simple Chain in the langchain with the help of the Chains.
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnableSequence

load_dotenv()


prompt1 = PromptTemplate(
    template="Generate the tweet about {topic}",
    input_variables=['topic']
)

prompt2 = PromptTemplate(
    template="Generate the Linkedin post about {topic}",
    input_variables=['topic']
)

model = ChatOpenAI(model='gpt-4o-mini')

parser = StrOutputParser()

parallel_chain = RunnableParallel({
    'tweet': RunnableSequence(prompt1, model, parser),
    'linkedin': RunnableSequence(prompt2, model, parser)
})

result = parallel_chain.invoke({'topic': 'AI'})

print(result['tweet'])
print("====" * 20)
print(result['linkedin'])
