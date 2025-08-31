from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage,AIMessage

load_dotenv()

model = ChatOpenAI(model="gpt-4.1-2025-04-14")

# for maintaining the history of the user and AI
chat_history = [
    SystemMessage(content="You are a helpful AI Assistant")
]

while True:
    user_input = input("You: ")
    chat_history.append(HumanMessage(content=user_input))
    if user_input == "exit":
        break
    result = model.invoke(chat_history)
    chat_history.append(AIMessage(content=result.content))
    print("AI: ", result.content)

print(chat_history)
