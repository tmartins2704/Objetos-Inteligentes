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
from utils_youtube import get_video_summary

st.set_page_config(
    page_title="Youtube Video Summarization", page_icon="./images/logo.png"
)
cols = st.columns([13, 150])
with cols[0]:
    st.image("./images/logo.png")
with cols[1]:
    st.title("Youtube Video Summarization")

st.markdown(
    """
    This page allows you to summarize a Youtube video using the PaLM API. 
    You can enter the URL of the video you want to summarize, and the PaLM API will generate a summary of the video.
    Make sure the video is public and contains the **v=** parameter in the URL.
    """
)

with st.form("video_form"):
    lang = st.selectbox("Select the language of summary:", ["pt", "es"])
    url = st.text_input("Enter the URL of the video you want to summarize:", 
                        "https://www.youtube.com/watch?v=gT4qqHMiEpA")

    submitted = st.form_submit_button("Submit")
    if submitted:
        with st.spinner("Generating summary..."):
            summary = get_video_summary(url, lang)

        st.success("Summary generated!")
        st.video(url)
        st.write("Summary:")
        st.markdown(summary)
