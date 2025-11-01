import streamlit as st
from langraph_backend import llm
from langraph_backend import chatbot
from langchain_core.messages import HumanMessage

# Config.
CONFIG = {'configurable': {'thread_id': "thread_1"}}

# st.session_state -> dict ->
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

# Load the conversation History.
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input = st.chat_input("Type Here")

if user_input:

    # First add the message to message_history
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)
    

    response = chatbot.invoke({'messages': [HumanMessage(content=user_input)]}, config=CONFIG)
    ai_message = response['messages'][-1].content
    # First add the message to message_history
    st.session_state['message_history'].append({'role': 'ai', 'content': ai_message})
    with st.chat_message('ai'):
        # response = llm.invoke(user_input)
        st.text(ai_message)
    


for message_chunk, metadata in chatbot.stream(
    {'messages': [HumanMessage(content="What is the receipe to make pasta")]},
    config = {'configurable': {'thread_id': "thread_1"}},
    stream_mode="messages"):

    if message_chunk.content:
        print(message_chunk.content, end=" ", flush=True)
