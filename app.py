import streamlit as st
import os
from utils.image_loader import load_images_from_folder
from pipeline.validation_pipeline import run_validation
from config.settings import UPLOAD_FOLDER, INPUT_IMAGE_FOLDER

st.set_page_config(page_title="Passport Photo Validator", layout="wide")

st.title("Passport Photo Validator")

images = load_images_from_folder()

col1, col2 = st.columns([1,2])

with col1:
    st.subheader("Select Dataset Image")

    selected_image = None

    if len(images) > 0:
        selected_image = st.selectbox(
            "Dataset Images",
            images
        )

    st.divider()

    st.subheader("Upload Image")

    uploaded_file = st.file_uploader(
        "Upload passport photo",
        type=["jpg","jpeg","png"]
    )

    if uploaded_file is not None:
        save_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)

        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        selected_image = save_path

with col2:
    st.subheader("Preview")

    if selected_image:

        if isinstance(selected_image, str) and os.path.exists(selected_image):
            image_path = selected_image
        else:
            image_path = os.path.join(INPUT_IMAGE_FOLDER, selected_image)

        st.image(image_path, width=350)

        if st.button("Validate Photo"):

            result = run_validation(image_path)

            if result["status"] == "Valid":
                st.success("Valid Passport Photo")
            else:
                st.error("Invalid Passport Photo")

            # Print validation flow in order
            if "flow" in result:
                for step in result["flow"]:
                    st.write(step)

            # Print reasons if invalid
            if result["status"] == "Invalid":
                for r in result["reasons"]:
                    st.write("-", r)    