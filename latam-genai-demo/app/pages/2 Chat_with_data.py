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
from configs import BQ_DATASET, BQ_TABLE, PROJECT_ID
from utils_bq import get_answer, run_query
from utils_streamlit import reset_st_state

# Set page configuration
st.set_page_config(page_title="Chat with Data", page_icon="./images/logo.png")

if reset := st.button("Reset Demo State"):
    reset_st_state()


cols = st.columns([13, 150])
with cols[0]:
    st.image("./images/logo.png")
with cols[1]:
    st.title("Chat with BigQuery table")

st.write(
    """
    This demo shows how to extract data from BigQuery using natural language and the PaLM API. 
    PaLM is a large language model from Google AI that can understand and respond to natural language queries. 
    By using PaLM, you can ask questions about your data in plain English, and PaLM will generate the 
    SQL queries necessary to retrieve the data.
    """
)

st.subheader("Data preview")
st.write("Preview of the table")


if preview_button := st.button("Preview table"):
    if "table_preview" not in st.session_state:
        with st.spinner("Loading preview table..."):
            st.session_state["table_preview"] = run_query(
                f"SELECT * FROM `{PROJECT_ID}.{BQ_DATASET}.{BQ_TABLE}` LIMIT 3"
            )

    st.dataframe(st.session_state["table_preview"])

st.divider()

st.subheader("Chat")
# Initialize chat history
if "data_messages" not in st.session_state:
    st.session_state.data_messages = []

# Display chat messages from history on app rerun
for message in st.session_state.data_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Qual o canal de marketing mais eficiente?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.data_messages.append({"role": "user", "content": prompt})

    response = get_answer(prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response["response"])
        st.markdown(response["query"])
        st.dataframe(response["table"])
    # Add assistant response to chat history
    st.session_state.data_messages.append(
        {"role": "assistant", "content": response["response"]}
    )
    st.session_state.data_messages.append(
        {"role": "assistant", "content": response["query"]}
    )
