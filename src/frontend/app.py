import streamlit as st
import sys
import os

# Fix path for imports
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from src.llm.agent import create_agent

st.set_page_config(page_title="Financial AI Agent", layout="centered")
st.title("📈 Financial Data Agent (Qwen)")

@st.cache_resource
def get_agent():
    return create_agent()

agent = get_agent()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about stocks (e.g. '600519.SH price')"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            try:
                response = agent.invoke({"input": prompt})
                st.markdown(response["output"])
                st.session_state.messages.append({"role": "assistant", "content": response["output"]})
            except Exception as e:
                st.error(f"Error: {str(e)}")