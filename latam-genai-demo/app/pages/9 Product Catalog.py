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

import json
import os

import pandas as pd
import streamlit as st
from utils_streamlit import reset_st_state
from utils_vertex import get_text_response_gemini

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DF_PATH = os.path.join(BASE_DIR, "sample_data", "products.json")
PROMPT_PATH = os.path.join(BASE_DIR, "prompts", "product_catalog.txt")

df = pd.read_json(DF_PATH)

with open(PROMPT_PATH, "r") as f:
    prompt = f.read()

# Set page configuration
st.set_page_config(page_title="Product Catalog", page_icon="./images/logo.png")

if reset := st.button("Reset Demo State"):
    reset_st_state()

cols = st.columns([13, 150])
with cols[0]:
    st.image("./images/logo.png")
with cols[1]:
    st.title("Product Catalog")

st.write(
    """
    This demo shows the usage of GenAI (embeddings and LLMs) to agument product catalog.
    Given a product name, product description and image of the product, Gemini Pro will provide
    an enhanced description for the product page. Using Vertex Vector Search and multimodal embeddings,
    it provides a list of the most similar products to yours.
    """
)

product_name = st.text_input("Enter the product name", placeholder="Ex: Relógio")
product_description = st.text_area("Enter the product description", placeholder="Ex: Usado")
product_image = st.file_uploader("Upload an image of the product", type=["png", "jpg", "jpeg"])

if st.button("Add Product"):
    with st.spinner("Adding your product to the catalog..."):
        prompt = prompt.format(product_name, product_description)
        response = get_text_response_gemini(prompt, images=[product_image.getvalue()])
        response = response.replace("```json", "").replace("```", "")
        data = json.loads(response)

        col1, col2 = st.columns([1, 4])

        with col1:
            st.image(product_image, caption=data["title"], use_column_width=True)

        with col2:
            st.markdown(f"### {data['title']}")
            st.markdown(f"**Descrição:** {data['description']}")
            markdown_table = "Atributo | Valor\n--- | ---\n"
            for key, value in data["attributes"].items():
                markdown_table += f"{key} | {value}\n"
            st.markdown(markdown_table)

    st.divider()

