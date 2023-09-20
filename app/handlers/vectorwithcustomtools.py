import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Neo4jVector
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
# from tools.databaseinspector import verify_database_structured
from langchain.agents.initialize import initialize_agent
from langchain.agents import AgentType
from langchain.schema import SystemMessage
from langchain.utilities import SearxSearchWrapper

from handlers.message import Message, write_message, save_question_and_response

embeddings = OpenAIEmbeddings()

vectorstore = Neo4jVector.from_existing_index(
    embedding=embeddings,
    index_name=st.secrets["NEO4J_VECTOR_INDEX_NAME"],
    url=st.secrets["NEO4J_HOST"],
    username=st.secrets["NEO4J_USERNAME"],
    password=st.secrets["NEO4J_PASSWORD"],
)

llm = ChatOpenAI(
    temperature=0,
    openai_api_key=st.secrets["OPENAI_API_KEY"],
)

memory = ConversationBufferMemory(memory_key="memory", return_messages=True)

system_message = SystemMessage(content="""
Your name is Elaine, your name stands for Educational Learning Assistant for Intelligent Network Exploration.
You are a friendly learning assistant teaching users to how use Neo4j.
Provide the user with simple, straightforward steps to help the user pass their current course, with code samples if possible.

Respond in Italian.
""")


# agent = initialize_agent(
#     tools = [ verify_database ],
#     llm=llm,
#     agent=AgentType.OPENAI_FUNCTIONS,
#     verbose=False,
#     system_message=system_message,
#     memory=memory
# )

# from langchain.schema import SystemMessage
from langchain.agents import OpenAIFunctionsAgent


prompt = OpenAIFunctionsAgent.create_prompt(system_message=system_message)


# from tools.databaseinspector import verify_database, VerifyDatabaseTool

from tools.databaseinspector.tool import DatabaseInspectorTool

from tools.wtf import CustomSearchTool

st.write(DatabaseInspectorTool.with_llm(llm))

# tools = [VerifyDatabaseTool()]
tools = [
    # verify_database
    # post_message_tool
    DatabaseInspectorTool.with_llm(llm),
    CustomSearchTool()
]


agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True,
    memory=memory,
)

def generate_response(prompt):
    message = Message("user", prompt)
    st.session_state.messages.append(message)

    write_message(message)

    with st.container():
        with st.spinner('Thinking...'):
            answer = agent.run(prompt)

            response = Message("assistant", answer)
            st.session_state.messages.append(response)

            write_message(response)
