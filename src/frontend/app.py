# app.py
import streamlit as st
import sys
import os
from langchain_core.messages import HumanMessage, AIMessage

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from src.llm.agent import create_agent

st.set_page_config(page_title="Financial AI Agent", layout="centered")
st.title("📈 Financial Data Agent")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        content = message["content"]
        if isinstance(content, str) and content.startswith("data:image"):
            st.image(content)
        else:
            st.markdown(content)

if prompt := st.chat_input("Ask about stocks (e.g., '600519.SH trend last 20 days')"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            try:
                agent = create_agent()
                
                # Convert Streamlit messages to LangChain format
                langchain_history = []
                for msg in st.session_state.messages:
                    if msg["role"] == "user":
                        langchain_history.append(HumanMessage(content=msg["content"]))
                    elif msg["role"] == "assistant":
                        langchain_history.append(AIMessage(content=msg["content"]))
                
                # Invoke agent with chat history
                response = agent.invoke({
                    "input": prompt,
                    "chat_history": langchain_history
                })
                
                answer = response.get("output", "")
                
                if isinstance(answer, str) and answer.startswith("data:image"):
                    st.image(answer)
                    st.markdown("*Historical trend chart generated.*")
                else:
                    st.markdown(answer)
                    
                st.session_state.messages.append({"role": "assistant", "content": answer})
                
            except Exception as e:
                st.error(f"System Error: {str(e)}")
                st.session_state.messages.append({"role": "assistant", "content": f"Error: {str(e)}"})