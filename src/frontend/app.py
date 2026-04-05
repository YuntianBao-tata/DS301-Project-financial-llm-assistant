# app.py
import streamlit as st
import sys
import os
import base64
import dashscope  # Native library for Qwen-VL (more stable for images)
from langchain_core.messages import HumanMessage, AIMessage

# Path setup
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from src.llm.agent import create_agent

st.set_page_config(page_title="Financial AI Agent", layout="centered")
st.title("📈 Financial AI Agent")

# --- Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Sidebar ---
with st.sidebar:
    st.header("📸 Visual Analysis")
    uploaded_file = st.file_uploader("Upload a chart", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

# --- Display History ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        content = message["content"]
        # Handle Base64 images (generated charts)
        if isinstance(content, str) and content.startswith("data:image"):
            st.image(content)
        # Handle Text
        elif isinstance(content, str):
            st.markdown(content)
        # Handle Multimodal Input (User uploaded image)
        elif isinstance(content, list):
            for item in content:
                if item.get("text"):
                    st.markdown(item["text"])
                elif item.get("image_url"):
                    st.image(item["image_url"]["url"], width=300)

# --- Main Logic ---
if prompt := st.chat_input("Ask about stocks..."):
    
    # 1. Prepare Input Content
    user_content = prompt
    is_vision_mode = False
    
    if uploaded_file:
        is_vision_mode = True
        try:
            bytes_data = uploaded_file.getvalue()
            base64_image = base64.b64encode(bytes_data).decode("utf-8")
            # Format for display and history
            user_content = [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
            ]
        except Exception as e:
            st.error(f"Image processing error: {e}")
            st.stop()

    # 2. Display User Message
    with st.chat_message("user"):
        if is_vision_mode:
            st.markdown(prompt)
            st.image(uploaded_file, width=300)
        else:
            st.markdown(prompt)
            
    # Add to history
    st.session_state.messages.append({"role": "user", "content": user_content})

    # 3. Generate Response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            try:
                answer = ""
                
                if is_vision_mode:
                    # --- PATH A: VISION MODE (Native DashScope) ---
                    # We use the native library to bypass LangChain's strict message formatting
                    dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")
                    
                    # Construct messages in OpenAI/DashScope format
                    messages = [
                        {
                            "role": "user",
                            "content": [
                                {"text": prompt},
                                {"image": f"data:image/jpeg;base64,{base64_image}"} # DashScope accepts base64 directly
                            ]
                        }
                    ]
                    
                    response = dashscope.MultiModalConversation.call(
                        model='qwen-vl-plus',
                        messages=messages
                    )
                    
                    if response.status_code == 200:
                        answer = response.output.choices[0].message.content[0]["text"]
                    else:
                        answer = f"Vision Error: {response.message}"

                else:
                    # --- PATH B: TEXT MODE (Standard Agent with Tools) ---
                    agent = create_agent(model_name="qwen-plus")
                    
                    # Convert history to LangChain objects
                    langchain_history = []
                    for msg in st.session_state.messages[:-1]:
                        # Filter for text only to avoid list errors in Agent
                        if isinstance(msg["content"], str) and not msg["content"].startswith("data:image"):
                            if msg["role"] == "user":
                                langchain_history.append(HumanMessage(content=msg["content"]))
                            elif msg["role"] == "assistant":
                                langchain_history.append(AIMessage(content=msg["content"]))

                    response = agent.invoke({
                        "input": prompt,
                        "chat_history": langchain_history
                    })
                    answer = response.get("output", "")

                # 4. Display Response
                if isinstance(answer, str) and answer.startswith("data:image"):
                    st.image(answer)
                    st.markdown("*Chart generated.*")
                else:
                    st.markdown(answer)
                    
                st.session_state.messages.append({"role": "assistant", "content": answer})
                
            except Exception as e:
                st.error(f"System Error: {str(e)}")