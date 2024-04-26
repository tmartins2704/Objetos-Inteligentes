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

import re

import streamlit as st
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from pypdf import PdfReader
from utils_streamlit import reset_st_state
from utils_vertex import embeddings, llm


def parse_pdf(pdf: str) -> str:
    pdf = PdfReader(pdf)
    output = []
    for page in pdf.pages:
        text = page.extract_text()
        # Merge hyphenated words
        text = re.sub(r"(\w+)-\n(\w+)", r"\1\2", text)
        # Fix newlines in the middle of sentences
        text = re.sub(r"(?<!\n\s)\n(?!\s\n)", " ", text.strip())
        # Remove multiple newlines
        text = re.sub(r"\n\s*\n", "\n\n", text)
        output.append(text)
    return "\n".join(output)


def get_pdf_chain(pdf):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len,
    )
    text = parse_pdf(pdf)
    text = text_splitter.split_text(text)
    vectorstore = FAISS.from_texts(text, embeddings)
    chain = RetrievalQA.from_chain_type(
        llm, chain_type="stuff", retriever=vectorstore.as_retriever()
    )
    return chain


st.set_page_config(page_title="Chat with PDFs", page_icon="./images/logo.png")

if reset := st.button("Reset Demo State"):
    reset_st_state()

cols = st.columns([13, 150])
with cols[0]:
    st.image("./images/logo.png")
with cols[1]:
    st.title("Chat with PDF")

st.write(
    """
    This demo shows how to chat with a PDF files using Gecko Embeddings and PALM text-bison.
    It uses  RAG (Retrival Augmented Generation) to retrieve the most relevant parts of the document to answer the question.
    """
)
# Upload PDF file
uploaded_file = st.file_uploader("Choose your .pdf file", type="pdf")

# Persists the chain in session_state
if uploaded_file is not None and "chain" not in st.session_state:
    with st.spinner("Processing your document..."):
        chain = get_pdf_chain(uploaded_file)
    st.success("Ready to chat!")
    st.session_state.chain = chain

# Initialize chat history
if "pdf_messages" not in st.session_state:
    st.session_state.pdf_messages = []

# Display chat messages from history on app rerun
for message in st.session_state.pdf_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask a question..."):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.pdf_messages.append({"role": "user", "content": prompt})
    chain = st.session_state.chain
    response = chain.run({"query": prompt})
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.pdf_messages.append({"role": "assistant", "content": response})
