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


import requests
from langchain.agents import AgentType, Tool, initialize_agent
from langchain.chains import RetrievalQA
from langchain.memory import ConversationBufferMemory
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_google_vertexai import VertexAI
from utils_vertex import embeddings, get_text_response_gemini
from utils_youtube import get_transcript

llm = VertexAI(model_name="text-bison-32k")


def video_qa(string: str) -> str:
    question, video_url = string.split(",")
    transcript = get_transcript(video_url, lang="en")
    with open("./prompts/video_qa.txt", "r") as f:
        prompt = f.read()
    prompt = prompt.format(transcript[:40000], question)
    text = llm(prompt)
    return text


def pdf_qa(string: str) -> str:
    question, pdf_url = string.split(",")
    loader = PyPDFLoader(pdf_url.strip())
    pages = loader.load_and_split()
    # Create a vector representation of each chunk from the PDF.
    vectordb = FAISS.from_documents(pages, embeddings)
    # Implementation of RAG on the PDF file provided by the user)
    qa = RetrievalQA.from_chain_type(
        llm=llm, chain_type="stuff", retriever=vectordb.as_retriever()
    )
    result = qa({"query": question})
    return result["result"]


def get_image_description(image_url: str) -> str:
    image = requests.get(image_url).content
    text = get_text_response_gemini("Describe this image:", [image])
    return text


# List of tools the agent will have access to, can be extended with other tools.
tools = [
    Tool(
        name="Image captioning",
        func=get_image_description,
        description="useful for when you recieve a image url to answer questions about that image. The function takes a parameter image_url (usually ending in .png, .jpeg, .gif or .jpg) and returns the description of that image in plain text",
    ),
    Tool(
        name="PDF Q&A tool",
        func=pdf_qa,
        description="useful for when you need to answer questions about a pdf document. The function takes 2 parameters pdf_url and question. The input to this tool should be a comma separated string, representing the question and the pdf_url. For example, `what is this pdf about, http://pdf.com` would be the input if you wanted to as what is this pdf about given this url http://pdf.com",
    ),
    Tool(
        name="Youtube video QA",
        func=video_qa,
        description="useful for when you need to answer questions about a pdf document. The function takes 2 parameters 'question' and 'video_url' (a youtube video url). The input to this tool should be a comma separated string, representing the question and the video_url. For example, `what is this video about, https://www.youtube.com/watch?v=CAOHTJ6sU4Q` would be the input if you wanted to as what is this pdf about given this url https://www.youtube.com/watch?v=CAOHTJ6sU4Q",
    ),
]


def get_agent():
    history = ConversationBufferMemory(memory_key="chat_history")
    agent_chain = initialize_agent(
        tools, llm, agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, memory=history
    )
    return agent_chain
