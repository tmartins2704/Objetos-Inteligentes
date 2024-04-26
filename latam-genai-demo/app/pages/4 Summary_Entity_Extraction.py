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

import pandas as pd
import streamlit as st
from utils_youtube import get_structured_video_info

st.set_page_config(page_title="Entity Extraction", page_icon="./images/logo.png")
cols = st.columns([13, 150])
with cols[0]:
    st.image("./images/logo.png")
with cols[1]:
    st.title("Video Entity Extraction")

st.markdown(
    """
    This demonstrates a usecase of video summarization and entity extraction. 
    You can enter the URL of the video you want to summarize, and the PaLM API will generate a summary of the video and extract pre determined entities.
    Make sure the video is public and contains the **v=** parameter in the URL. Define the entities below in the json format.
    """
)

with st.form("video_form"):
    entities = st.text_area(
        "Add entities to extract:",
        "{\n"
        '  "name": "name of the customer",\n'
        '  "summary": "the summary of the video",\n'
        '  "credit_card_type": "type of card mentioned in the video",\n'
        '  "last_4_digits": "last 4 digits of the card mentioned in the video",\n'
        '  "date": "date of the incident",\n'
        '  "transactions": "total number of transactions",\n'
        '  "amount": "total amount"\n'
        "}\n",
    )
    url = st.text_input(
        "Enter the URL of the Youtube video",
        "https://www.youtube.com/watch?v=CAOHTJ6sU4Q",
    )
    lang = st.selectbox("Select the language of the video", ["pt", "es", "en"])
    submitted = st.form_submit_button("Submit")
    if submitted:
        with st.spinner("Generating summary..."):
            summary = get_structured_video_info(url, lang, entities)

        st.success("Summary generated!")
        st.video(url)
        st.write("Summary:")
        st.write(summary["summary"])
        df = pd.DataFrame.from_dict(summary, orient="index", columns=["value"])
        st.dataframe(df, use_container_width=True)
