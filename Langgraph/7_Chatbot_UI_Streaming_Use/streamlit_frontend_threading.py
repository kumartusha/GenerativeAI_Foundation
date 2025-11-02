import streamlit as st
from langraph_backend import llm
from langraph_backend import chatbot
from langchain_core.messages import HumanMessage

# used for dynamic creating the thread ID.
import uuid

# ******************************** Utility Functions ***********************************
def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id

# Implement the Task 2nd from the md file.
def reset_chat():
    thread_id = generate_thread_id()

    st.session_state['thread_id'] = thread_id

    # add all the thread_id into the session_state thread List.
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history'] = []


def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_conversation(thread_id):
    return chatbot.get_state(config={'configurable': {'thread_id': thread_id}}).values['messages']


# *********************************** Session Setup ***********************************
# st.session_state -> dict ->
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = []

# add the thread_id whenever page reloaded.
add_thread(st.session_state['thread_id'])

# ************************************ Sidebar UI *************************************
st.sidebar.title("Langraph Chatbot")

if st.sidebar.button("New Chat"):
    reset_chat()

# add all the thread id which is store in the session_state thread list.
st.sidebar.header("My Conversations")
for thread_id in st.session_state['chat_threads'][::-1]:
    if st.sidebar.button(str(thread_id)):
        # Return list of messages.
        st.session_state['thread_id'] = thread_id
        messages = load_conversation(thread_id)

        # convert HumanMessage[] format output to the proper session history for loading the chat. 
        temp_messages = []

        for msg in messages:
            if isinstance(msg, HumanMessage):
                role = 'user'
            else:
                role = 'ai'
            temp_messages.append({'role': role, 'content': msg.content})



# ************************************* Main UI ***************************************
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
    
    CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}
    # First add the message to message_history
    # st.session_state['message_history'].append({'role': 'ai', 'content': ai_message})
    with st.chat_message('ai'):

        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config = CONFIG,
                stream_mode="messages"
            )
        )
        # Store in the session_state
        st.session_state['message_history'].append({'role': 'ai', 'content': ai_message})