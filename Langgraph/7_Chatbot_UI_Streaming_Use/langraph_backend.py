from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import operator
from langgraph.graph.message import add_messages
import os
from langgraph.checkpoint.memory import InMemorySaver
import os

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


# Check pointer
checkpointer = InMemorySaver()

# Create the graph.
graph = StateGraph(ChatState)


# Add nodes

graph.add_node('chat_node', chat_node)


# Add edges.
graph.add_edge(START, 'chat_node') 
graph.add_edge('chat_node', END)

chatbot = graph.compile(checkpointer=checkpointer)