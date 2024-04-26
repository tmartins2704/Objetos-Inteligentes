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

from io import BytesIO

import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas
from utils_vertex import get_text_response_gemini

st.set_page_config(page_title="Image Captionign", page_icon="./images/logo.png")
cols = st.columns([13, 150])
with cols[0]:
    st.image("./images/logo.png")
with cols[1]:
    st.title("Image Captioning")

st.markdown(
    """
    This demo uses Google Gemini Pro to describe hand drawn images. 
    Use the tools on the left to draw your image and hit Send Image.
    """
)

# Specify canvas parameters in application
drawing_mode = st.sidebar.selectbox(
    "Drawing tool:", ("freedraw", "line", "rect", "circle", "transform")
)

stroke_width = st.sidebar.slider("Stroke width: ", 1, 25, 3)
stroke_color = st.sidebar.color_picker("Stroke color hex: ")
bg_color = st.sidebar.color_picker("Background color hex: ", "#eee")
bg_image = st.sidebar.file_uploader("Background image:", type=["png", "jpg"])
send_image = st.sidebar.checkbox("Update in realtime", True)

# Create a canvas component
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    background_image=Image.open(bg_image) if bg_image else None,
    update_streamlit=send_image,
    height=500,
    drawing_mode=drawing_mode,
    key="canvas",
)

if send := st.button("Send Image"):
    image = BytesIO()
    pil_img = Image.fromarray(canvas_result.image_data)
    rgb_im = pil_img.convert("RGB")
    rgb_im.save(image, format="JPEG")

    if canvas_result.image_data is not None:
        with st.spinner("Processing your Image..."):
            description = get_text_response_gemini(
                "Describe this drawing as best as you can", [image.getvalue()]
            )
        st.success("Done!")
        st.write("Description:")
        st.write(description)
