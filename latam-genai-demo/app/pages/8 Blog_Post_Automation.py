import concurrent.futures
import io
import json
import os
import time
import uuid

import jinja2
import streamlit as st
from utils_storage import upload_image_to_gcs
from utils_vertex import get_text_response_gemini, imagen

# Define paths relative to the script location
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
BLOG_HTML_PATH = os.path.join(TEMPLATES_DIR, "blog.html")
PROMPT_PATH = os.path.join(BASE_DIR, "prompts", "blog.txt")

# Initialize session state for user_id
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())


def read_template():
    """Read and return the prompt template."""
    with open(PROMPT_PATH, "r") as file:
        return file.read()


def generate_and_save_image(prompt, file_name, size):
    """Generate an image from a prompt, save it, and return a signed URL."""
    try:
        images = imagen.generate_images(prompt=prompt, number_of_images=1, seed=1)
    except Exception as e:
        print(f"Error generating image: {e}")
        print(prompt)
        return {"url": "no_image", "file_name": file_name}

    image = images[0]._pil_image.resize(size)

    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format="JPEG")
    img_byte_arr.seek(0)

    signed_url = upload_image_to_gcs(img_byte_arr.getvalue(), file_name)
    return {"url": signed_url, "file_name": file_name}


# Generate images in parallel
def generate_images_in_parallel(prompts, sizes):
    """Generate images in parallel, returning their signed URLs."""
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = [
            executor.submit(
                generate_and_save_image,
                prompt,
                f"{i}.{st.session_state.user_id}.jpg",
                size,
            )
            for i, (prompt, size) in enumerate(zip(prompts, sizes))
        ]
        return [future.result() for future in concurrent.futures.as_completed(futures)]


def generate_post(data):
    """Generate the blog post with images and save it to an HTML file."""
    prompts = [data["blog_title"]] + data["steps_prompts"]
    sizes = [(1920, 1080)] + [(300, 300)] * len(data["steps_prompts"])
    files = generate_images_in_parallel(prompts, sizes)
    files = sorted(files, key=lambda d: d["file_name"])
    urls = [file["url"] for file in files]

    data["header_image_url"], data["steps_images"] = urls[0], urls[1:]
    data["timestamp"] = int(time.time())

    template_loader = jinja2.FileSystemLoader(searchpath=TEMPLATES_DIR)
    template_env = jinja2.Environment(loader=template_loader)
    template_env.globals.update(zip=zip)
    template = template_env.get_template("template_blog.html")
    output_text = template.render(data)

    with open(BLOG_HTML_PATH, "w") as html_file:
        html_file.write(output_text)


def display_html_file():
    """Display the generated HTML file."""
    with open(BLOG_HTML_PATH, "r") as file:
        html_content = file.read()
    st.components.v1.html(html_content, width=700, height=800, scrolling=True)


st.set_page_config(page_title="Blog Post Automation", page_icon="./images/logo.png")
st.title("Blog Post Automation")

st.write("This app demonstrates how to create a blog post about a dish using AI.")
dish_name = st.text_input(
    "Enter the name of the dish:", placeholder="Ex: chocolate mousse"
)

if st.button("Generate Post"):
    if not dish_name:
        st.warning("Please enter the name of the dish.")
        st.stop()

    with st.spinner("Creating Blog Post..."):
        prompt = read_template()
        response = get_text_response_gemini(prompt.format(dish_name), [])
        data = json.loads(response.replace("```json", "").replace("```", ""))
        generate_post(data)

    st.success("Blog post created successfully!")
    display_html_file()
