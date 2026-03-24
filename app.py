# import streamlit as st
# import os
# from utils.image_loader import load_images_from_folder
# from pipeline.validation_pipeline import run_validation
# from config.settings import UPLOAD_FOLDER, INPUT_IMAGE_FOLDER

# st.set_page_config(page_title="Passport Photo Validator", layout="wide")

# st.title("Passport Photo Validator")

# images = load_images_from_folder()

# col1, col2 = st.columns([1, 2])

# with col1:
#     st.subheader("Select Dataset Image")

#     selected_image = None

#     if images:
#         if "image_index" not in st.session_state:
#             st.session_state.image_index = 0

#         selected_image = st.selectbox(
#             "Dataset Images",
#             images,
#             index=st.session_state.image_index
#         )

#         st.session_state.image_index = images.index(selected_image)

#         prev_col, next_col = st.columns(2)
#         with prev_col:
#             if st.button("← Prev", use_container_width=True):
#                 if st.session_state.image_index > 0:
#                     st.session_state.image_index -= 1
#                     st.rerun()
#         with next_col:
#             if st.button("Next →", use_container_width=True):
#                 if st.session_state.image_index < len(images) - 1:
#                     st.session_state.image_index += 1
#                     st.rerun()

#     st.divider()

#     st.subheader("Upload Image")

#     uploaded_file = st.file_uploader(
#         "Upload passport photo",
#         type=["jpg", "jpeg", "png"]
#     )

#     if uploaded_file is not None:
#         save_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
#         with open(save_path, "wb") as f:
#             f.write(uploaded_file.getbuffer())
#         selected_image = save_path

# with col2:
#     st.subheader("Preview")

#     if selected_image:
#         image_path = selected_image if os.path.exists(selected_image) else os.path.join(INPUT_IMAGE_FOLDER, selected_image)

#         st.image(image_path, width=350)

#         if st.button("Validate Photo"):
#             result = run_validation(image_path)

#             if result["status"] == "Valid":
#                 st.success("Valid Passport Photo")
#             else:
#                 st.error("Invalid Passport Photo")

#             if "flow" in result:
#                 for step in result["flow"]:
#                     st.write(step)

#             if result["status"] == "Invalid":
#                 for r in result["reasons"]:
#                     st.write("-", r)





import streamlit as st
import os
import cv2
from utils.image_loader import load_images_from_folder
from pipeline.validation_pipeline import run_validation
from config.settings import UPLOAD_FOLDER, INPUT_IMAGE_FOLDER

st.markdown("""
<style>
[data-testid="stFileUploader"] small {
    display: none;
}
</style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="Passport Photo Validator", layout="wide")

st.title("Passport Photo Validator")

images = load_images_from_folder()

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Select Dataset Image")

    selected_image = None

    if images:
        if "image_index" not in st.session_state:
            st.session_state.image_index = 0

        selected_image = st.selectbox(
            "Dataset Images",
            images,
            index=st.session_state.image_index
        )

        st.session_state.image_index = images.index(selected_image)

        prev_col, next_col = st.columns(2)

        with prev_col:
            if st.button("← Prev", use_container_width=True):
                if st.session_state.image_index > 0:
                    st.session_state.image_index -= 1
                    st.rerun()

        with next_col:
            if st.button("Next →", use_container_width=True):
                if st.session_state.image_index < len(images) - 1:
                    st.session_state.image_index += 1
                    st.rerun()

    st.divider()

    st.subheader("Upload Image")

    st.caption("Max file size: 300KB • JPG, JPEG, PNG")

    uploaded_file = st.file_uploader(
        "Upload passport photo",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:
        save_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        selected_image = save_path

with col2:
    st.subheader("Preview")

    if selected_image:
        image_path = selected_image if os.path.exists(selected_image) else os.path.join(INPUT_IMAGE_FOLDER, selected_image)

        # 🔥 STEP 1: show image instantly
        st.image(image_path, width=350)

        st.markdown("---")

        # 🔥 STEP 2: validation only on button click
        validate_clicked = st.button("Validate Photo")

        if validate_clicked:
            with st.spinner("Validating..."):
                result = run_validation(image_path)

            if result["status"] == "Valid":
                st.success("Valid Passport Photo")
            else:
                st.error("Invalid Passport Photo")

            if "flow" in result:
                for step in result["flow"]:
                    st.write(step)

            if result["status"] == "Invalid":
                for r in result["reasons"]:
                    st.write("-", r)