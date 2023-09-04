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
from handlers.vectorconversation import generate_response


if "messages" not in st.session_state:
    st.session_state.last_message = None
    st.session_state.feedback_form = None
    st.session_state.messages = [
        Message("assistant", "Hi, I'm the GraphAcademy Chatbot!  How can I help you?"),
    ]

with st.container():
    for message in st.session_state.messages:
        write_message(message)




prompt = st.chat_input("What's up?")

if prompt:
    generate_response(prompt)
