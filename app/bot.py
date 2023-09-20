import streamlit as st
from handlers.message import Message, write_message

# from chatbot import handle_submit
# from typing_extensions import Generator

st.set_page_config("GraphAcademy Chatbot")

# from handlers.openai import generate_response
# from handlers.neo4jvector import generate_response
# from handlers.openaichat import generate_response
# from handlers.neo4jrag.handler import generate_response
# from handlers.openaichatvector import generate_response
# from handlers.vectorconversation import generate_response
from handlers.vectorwithcustomtools import generate_response


if "messages" not in st.session_state:
    st.session_state.last_message = None
    st.session_state.feedback_form = None
    st.session_state.messages = [
        Message("assistant", "Hi, I'm the GraphAcademy Chatbot!  How can I help you?"),
    ]
    # st.session_state.sandbox_uri = 'bolt+s://7c4bc4489aa82e8653601ca05b7a4b25.neo4jsandbox.com:7687'
    # st.session_state.sandbox_username = 'neo4j'
    # st.session_state.sandbox_password = 'diseases-groom-door'

def form_callback():
    st.write(st.session_state.sandbox_uri)

with st.expander('Context'):
    with st.form('context'):
        sandbox_uri = st.text_input('Sandbox Host', 'neo4j://44.203.228.186:7687', key='sandbox_uri')
        sandbox_username = st.text_input('Username', 'neo4j', key='sandbox_username')
        sandbox_password = st.text_input('Password', 'diseases-groom-door', key='sandbox_password')
        submit_button = st.form_submit_button(label='Submit', on_click=form_callback)


with st.container():
    for message in st.session_state.messages:
        write_message(message)




prompt = st.chat_input("What's up?")

if prompt:
    generate_response(prompt)
