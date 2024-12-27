import streamlit as st
from agents.repoagent import repo_agent

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
