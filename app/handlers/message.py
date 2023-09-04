import streamlit as st
from datetime import datetime
from typing import Literal

from neo4j import GraphDatabase

driver = GraphDatabase.driver(
    st.secrets['NEO4J_HOST'],
    auth=(st.secrets['NEO4J_USERNAME'], st.secrets['NEO4J_PASSWORD'])
)

class Message:
    def __init__(self, role: Literal["user", "assistant"], content: str, documents = []):
        self.role = role
        self.timestamp = datetime.now()
        self.content = content
        self.documents = documents

def write_message(message):
    with st.chat_message(message.role):
        st.markdown(f"**{datetime.now().strftime('%H:%M:%S')}**: {message.content}")


def save_question_and_response(question, response, documents):
    with driver.session() as session:
        sections = [ {"sectionUrl": d.metadata["url"]} for d in documents ]

        res = session.execute_write(lambda tx: tx.run("""
            CREATE (r:Response:StreamlitResponse {
                id: randomUuid(),
                createdAt: datetime(),
                question: $question,
                embedding: $embedding,
                response: $response
            })

            FOREACH (_ IN CASE WHEN $page IS NOT NULL THEN [1] ELSE [] END |
                MERGE (p:Page {url: $page})
                MERGE (r)-[:FROM_PAGE]->(p)
            )

            FOREACH (section IN $sections |
                MERGE (s:Section {url: section.sectionUrl})
                MERGE (r)-[sr:SUGGESTED_SECTION]->(s)
            )

            RETURN r.id AS id
        """, page = None, question=question, response=response, embedding = None, sections=sections).single())

        return res.get("id")
