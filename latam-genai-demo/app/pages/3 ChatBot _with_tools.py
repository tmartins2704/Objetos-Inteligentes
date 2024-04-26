# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import streamlit as st
from utils_agents import get_agent
from utils_streamlit import reset_st_state

# Set page configuration
st.set_page_config(page_title="LangChain Agents", page_icon="./images/logo.png")

if reset := st.button("Reset Demo State"):
    reset_st_state()

cols = st.columns([13, 150])
with cols[0]:
    st.image("./images/logo.png")
with cols[1]:
    st.title("Chat Bot with Tools")

st.write(
    """
    This page provides an example of a ChatBot Assistant capable of using tools based on the ReAct prompt style.
    Tools are custom functions that provide the Bot a way to extend its capabilities by interacting with APIs.
    In this particular example, the Bot is capable of the following tasks:

    - Answer questions about an image, provide the image url alongside your question, for example: "What is the image? https://image_url.com"
    - Answer questions about a video, provide the video url alongside your question, for example: "What is the video about? https://www.youtube.com/watch?v="
    - Answer questions about a PDF file, provide the PDF file url alongside your question, for example: "your question about pdf? https://pdf_url.com"
    """
)

st.divider()

# Initialize chat history
if "agent_messages" not in st.session_state:
    st.session_state.agent_messages = []
    agent = get_agent()
    st.session_state.agent = agent

# Display chat messages from history on app rerun
for message in st.session_state.agent_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask a question..."):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    content = prompt.split(" ")[-1].strip()

    if content.split(".")[-1] in ["jpg", "png", "gif"]:
        st.image(content)
    elif "v=" in content:
        st.video(content)

    # Add user message to chat history
    st.session_state.agent_messages.append({"role": "user", "content": prompt})

    response = st.session_state.agent.run(prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.agent_messages.append({"role": "assistant", "content": response})
