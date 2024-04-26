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
import utils_streamlit

st.set_page_config(page_title="GenAI LATAM Demos", page_icon="./images/logo.png")

cols = st.columns([12, 85])
with cols[0]:
    st.image("./images/logo.png")
with cols[1]:
    st.title("Generative AI - LATAM Demos")

reset = st.button("Reset Demo State")

if reset:
    utils_streamlit.reset_st_state()

st.subheader("Demonstrations")
st.write("Select a page from the left side menu to start one of the demos. They all should work in Portuguese and Spanish.")
st.write("Description of each demonstration:")
st.write(
    """**1. Chat with PDF**: Upload a .pdf file and have a conversation with it.\n
**2. Chat with data**: Select a BigQuery table and ask questions in natural language.\n
**3. ChatBot with tools**: Chat with a bot capable of multiple tasks by using the ReAct prompt style.\n
**4. Youtube Video Summarization**: Select a Youtube video and have the model summarize it.\n
**5. Summary and Entity Extraction**: You can enter the URL of the video you want to summarize, and the PaLM API will generate a summary of the video and extract pre determined entities.\n
**6. Image Captioning**: Draw something in the canvas and have the model generate a caption for it.\n
**7. News Sentiment Analysis**: Uses PALM to extract entities and analyze news articles.\n
**8. Blog Post Automation**: Uses Gemini and Imagen to automate a blog post for cooking recipies. \n
**9. Customer Complaints Analysis**: Uses PALM and Gecko Embeddings to analyze, summarize and cluster customer complaints. \n
**10. Product Catalog**: Uses Gemini to create better product descriptions and shows a text to image similarity search.
"""
)
