import streamlit as st
from langchain.llms import OpenAI
from handlers.message import Message, write_message

llm = OpenAI(temperature=0.7, openai_api_key=st.secrets["OPENAI_API_KEY"])

def generate_response(prompt):
    message = Message("user", prompt)
    st.session_state.messages.append(message)

    write_message(message)

    with st.spinner('Thinking...'):
        response = Message("assistant", llm(prompt))

        st.session_state.messages.append(response)

        write_message(response)
