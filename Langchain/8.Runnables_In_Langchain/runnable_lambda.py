# from langchain.schema.runnable import RunnableLambda

# def word_counter(text):
#     return len(text.split())


# runnable_word_counter = RunnableLambda(word_counter)

# print(runnable_word_counter.invoke("Hello guys how are you buddy"))


# Here we will be implement the Simple Chain in the langchain with the help of the Chains.
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence, RunnablePassthrough, RunnableParallel
from langchain.schema.runnable import RunnableLambda

load_dotenv()

# we initialize the model.
model = ChatOpenAI(model="gpt-4o-mini")

parser = StrOutputParser()

def word_count(text):
    return len(text.split())

prompt = PromptTemplate(
    template="Generate the joke about the {topic}",
    input_variables=['topic']
)

joke_gen = RunnableSequence(prompt, model, parser)

parallel_chain = RunnableParallel({
    'joke': RunnablePassthrough(),
    'word_count': RunnableLambda(word_count)
})
# parallel_chain = RunnableParallel({
#     'joke': RunnablePassthrough(),
#     'word_count': RunnableLambda(lambda x: len(x.split()))
# })

final_chain = RunnableSequence(joke_gen, parallel_chain)

result = final_chain.invoke({"topic": 'HFT Trading'})

print(result)