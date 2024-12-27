import streamlit as st
from phi.agent import RunResponse
from typing import Iterator
from src.agents.repo_agent import repo_agent
from src.static.repo_static import repo_static


repo_static.update_repo_details(username='sufyan-555',repo='ExpertConnect')

st.title("GitHub Repo Agent")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is your query?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = repo_agent.run(prompt)
        message_placeholder.markdown(full_response.content)
        st.session_state.messages.append({"role": "assistant", "content": full_response.content})
