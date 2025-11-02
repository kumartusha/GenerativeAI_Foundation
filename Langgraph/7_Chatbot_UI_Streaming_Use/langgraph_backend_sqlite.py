########     STEPS     #######
# -> create new frontend and backend file.
# -> install langgraph-checkpoint-sqlite
# -> implement database in backend
# -> chat in multiple threads
# install and visualize
# -> integrate to frontend

from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import operator
from langgraph.graph.message import add_messages
import os
from langgraph.checkpoint.sqlite import SqliteSaver
import os
import sqlite3

load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-120b", api_key=os.getenv("GROK_API_KEY"))

class ChatState(TypedDict):
    # AIMessage, HumanMessage, SystemMessage these are inherit the Basemessage means in the list
    # any type of message will be contain or add the reducer function because we need to merge them.

    # Always use addmessages its same as the operator.add but it is optimize one that working well 
    # with the add_messages.
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state: ChatState):

    # take user query from state.
    messages = state['messages']

    # send to the llm
    response = llm.invoke(messages)

    # Response store state.

    return {'messages': [response]}

# Create the sqlite database and checkpointer store the values in the database.
conn = sqlite3.connect(database='chatbot.db', check_same_thread=False)
# Check pointer
checkpointer = SqliteSaver(conn=conn)

# Create the graph.
graph = StateGraph(ChatState)


# Add nodes
graph.add_node('chat_node', chat_node)


# Add edges.
graph.add_edge(START, 'chat_node') 
graph.add_edge('chat_node', END)

chatbot = graph.compile(checkpointer=checkpointer)

def retreive_all_thread_from_database():
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])
        
    return list(all_threads)

# #Testing Code
# CONFIG = {'configurable': {'thread_id': 'thread-2'}}
#     # First add the message to message_history
#     # st.session_state['message_history'].append({'role': 'ai', 'content': ai_message})
# response = chatbot.invoke(
#             {'messages': [HumanMessage(content="what is HFT arbitrage ?")]},
#             config = CONFIG
#         )

# print(response)