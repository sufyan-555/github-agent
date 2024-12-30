import streamlit as st
from src.static.repo_static import repo_static
from src.agents.crew import crew
from pprint import pprint

st.set_page_config(layout="wide")

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    username = st.text_input("GitHub Username")
    repo_id = st.text_input("Repository ID")

if username and repo_id:
    repo_static.update_repo_details(username, repo_id)

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if prompt := st.chat_input("What is your query?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            with st.spinner("Processing..."):
                full_response = crew.run(prompt)
            message_placeholder.markdown(full_response.content)
            st.session_state.messages.append({"role": "assistant", "content": full_response.content})
else:
    st.warning("Please enter the GitHub username and repository Id to begin")
