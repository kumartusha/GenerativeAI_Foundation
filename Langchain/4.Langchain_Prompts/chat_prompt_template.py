from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage


chat_prompt_template = ChatPromptTemplate([
    ('system', 'You are a helpful {domain} expert'),
    ('human', 'Explain in simple term what is {topic}')
])


prompt = chat_prompt_template.invoke({'domain': 'finance', 'topic': 'Trading'})

print(prompt)