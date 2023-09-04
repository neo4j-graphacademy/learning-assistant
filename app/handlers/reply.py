import streamlit as st
import time
from handlers.message import Message, write_message

def generate_response(prompt):
    message = Message("user", prompt)
    st.session_state.messages.append(message)

    write_message(message)

    with st.spinner('Thinking...'):
        time.sleep(1)

        response = Message("assistant", prompt)
        st.session_state.messages.append(response)

        write_message(response)
