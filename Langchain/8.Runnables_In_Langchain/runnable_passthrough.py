# Here we will be implement the Simple Chain in the langchain with the help of the Chains.
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnableSequence, RunnablePassthrough

load_dotenv()

# passthrough = RunnablePassthrough()

# result = passthrough.invoke({'name': 'nitish', 'age': 36})

# print(result)

# we initialize the model.
model = ChatOpenAI(model="gpt-4o-mini")

parser = StrOutputParser()

template1 = PromptTemplate(
    template="Generate the joke about the {topic}",
    input_variables=['topic']
)

template2 = PromptTemplate(
    template="Explain the following Joke {text}",
    input_variables=['text']
)

joke_gen_chain = RunnableSequence(template1, model, parser)

parallel_chain = RunnableParallel({
    'joke': RunnablePassthrough(),
    'explanation': RunnableSequence(template2, model, parser)
})

final_chain = RunnableSequence(joke_gen_chain, parallel_chain)


result = final_chain.invoke("HFT Trading")

print(result)









