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
import plotly.express as px
import streamlit as st
from utils_streamlit import reset_st_state

# Set page configuration
st.set_page_config(page_title="News Sentiment Analysis", page_icon="./images/logo.png")

if reset := st.button("Reset Demo State"):
    reset_st_state()

cols = st.columns([13, 150])
with cols[0]:
    st.image("./images/logo.png")
with cols[1]:
    st.title("News Sentiment Analysis and Clustering")

st.markdown(
    """
    This demo shows how PALM text-bison can be used to perform sentiment analysis on news articles.
    It also extracts entities from the headlines. 
    Finally it uses Gecko Embeddings to cluster the articles by similarity and visualize the results.
    """
)

df = pd.read_json("data.json")

df2 = df.copy()
df2 = df2[["headline", "sentiment", "x", "y", "cluster"]]

fig = px.scatter(df2, x="x", y="y", color="cluster", hover_name="headline")
fig.layout.update(showlegend=False)

st.plotly_chart(fig, theme=None, use_container_width=True)

st.dataframe(
    df[["date", "headline", "source", "sentiment", "entities"]],
    use_container_width=True,
)
