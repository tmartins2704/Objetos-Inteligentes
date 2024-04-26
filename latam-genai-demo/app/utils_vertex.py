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

import vertexai
from configs import PROJECT_ID
from google.cloud import aiplatform
from langchain_google_vertexai import VertexAI, VertexAIEmbeddings
from vertexai.language_models import TextGenerationModel
from vertexai.preview.generative_models import GenerativeModel
from vertexai.preview.generative_models import Image as GenImage
from vertexai.preview.vision_models import Image as VisionImage
from vertexai.preview.vision_models import (
    ImageGenerationModel,
    MultiModalEmbeddingModel,
)

aiplatform.init(project=PROJECT_ID, location="us-central1")
vertexai.init(project=PROJECT_ID)


llm = VertexAI(model_name="text-bison")
imagen = ImageGenerationModel.from_pretrained("imagegeneration@005")
embeddings = VertexAIEmbeddings(model_name="textembedding-gecko-multilingual@latest")
multimodal_embeddings = MultiModalEmbeddingModel.from_pretrained(
    "multimodalembedding@001"
)

def get_text_response(prompt: str, model: str = "text-bison") -> str:
    text_model = TextGenerationModel.from_pretrained(model)
    response = text_model.predict(prompt, temperature=0.2, max_output_tokens=1024)
    text = response.text
    return text


def get_text_response_gemini(
    text_prompt: str, images: list = [], model: str = "gemini-pro-vision"
) -> str:
    images = [GenImage.from_bytes(data) for data in images[:15]]
    model = GenerativeModel(model)
    response = model.generate_content(
        [text_prompt, *images],
        generation_config={
            "max_output_tokens": 2048,
            "temperature": 0.1,
            "top_p": 1,
            "top_k": 32,
        },
        stream=False,
    )
    text = response.text
    return text


def get_multimodal_embeddings(text: str = None, image: bytes = None) -> list:
    if image:
        embeddings = multimodal_embeddings.get_embeddings(VisionImage(image), text)
        embeddings = embeddings.image_embedding
    else:
        embeddings = multimodal_embeddings.get_embeddings(None, text)
        embeddings = embeddings.text_embedding
    return embeddings
