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
    
    
    # First add the message to message_history
    # st.session_state['message_history'].append({'role': 'ai', 'content': ai_message})
    with st.chat_message('ai'):

        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config = {'configurable': {'thread_id': "thread_1"}},
                stream_mode="messages"
            )
        )
        # Store in the session_state
        st.session_state['message_history'].append({'role': 'ai', 'content': ai_message})