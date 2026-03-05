import streamlit as st
import os
from utils.image_loader import load_images_from_folder, load_image_by_index
from pipeline.validation_pipeline import run_validation
from config.settings import UPLOAD_FOLDER

st.set_page_config(page_title="Passport Photo Validator", layout="wide")

if "image_index" not in st.session_state:
    st.session_state.image_index = 0

images = load_images_from_folder()

st.title("Passport Size Photo Validator")

st.subheader("Dataset Image Testing")

col1, col2 = st.columns(2)

with col1:
    if st.button("Previous"):
        if st.session_state.image_index > 0:
            st.session_state.image_index -= 1

with col2:
    if st.button("Next"):
        if st.session_state.image_index < len(images) - 1:
            st.session_state.image_index += 1

if len(images) > 0:
    image, path = load_image_by_index(st.session_state.image_index, images)
    st.image(image, caption=images[st.session_state.image_index], width=300)
    if st.button("Predict"):
        result = run_validation(path)

        if result["status"] == "Valid":
            st.success("Valid Passport Photo")
        else:
            st.error("Invalid Passport Photo")
            for r in result["reasons"]:
                st.write("-", r)

st.divider()

st.subheader("Upload Image")

uploaded_file = st.file_uploader("Upload a photo", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:

    save_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)

    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.image(save_path, caption="Uploaded Image", width=300)

    if st.button("Validate Uploaded Image"):
        result = run_validation(save_path)

        if result["status"] == "Valid":
            st.success("Valid Passport Photo")
        else:
            st.error("Invalid Passport Photo")
            for r in result["reasons"]:
                st.write("-", r)