import streamlit as st
from typing import Optional
from neo4j import GraphDatabase

driver = GraphDatabase.driver(
    st.secrets['NEO4J_HOST'],
    auth=(st.secrets['NEO4J_USERNAME'], st.secrets['NEO4J_PASSWORD'])
)

def save_feedback(driver, id: str, helpful: bool, reason: Optional[str], additional: Optional[str]):
    with driver.session() as session:
        session.execute_write(lambda tx: tx.run("""
            MATCH (r:Response {id: $id})
            SET r.helpful = $helpful
            FOREACH (_ IN CASE WHEN $helpful = true THEN [1] ELSE [] END |
                SET r:HelpfulResponse
            )
            FOREACH (_ IN CASE WHEN $helpful = false THEN [1] ELSE [] END |
                SET r:UnhelpfulResponse
                SET r.reason = $reason,
                    r.additional = $additional,
                    r.feedbackProvidedAt = datetime()
            )
            RETURN r.id AS id
        """, id=id, helpful=helpful, reason=reason, additional=additional).consume())


def feedback_form(id):
    feedback_placeholder = st.empty()
    form = feedback_placeholder.form(id)
    helpful = form.selectbox(label="Was this answer helpful?", options=["Yes", "No"])
    reason = form.selectbox('Reason', options=[
        'missing', 'inaccurate', 'hard-to-follow', 'other'
    ])
    additional = form.text_input('Additional Information')

    def handle_submit():
        with st.spinner('Saving Feedback...'):
            feedback_placeholder.empty()
            save_feedback(driver, id, helpful is True, reason, additional)

            st.info( (helpful, reason, additional))

    form.form_submit_button("Save Feedback ", on_click=handle_submit)

    return feedback_placeholder
