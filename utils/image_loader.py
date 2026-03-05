import os
from PIL import Image
from config.settings import INPUT_IMAGE_FOLDER


def load_images_from_folder():
    files = []
    for file in os.listdir(INPUT_IMAGE_FOLDER):
        if file.lower().endswith((".jpg", ".jpeg", ".png")):
            files.append(file)
    files.sort()
    return files


def load_image_by_index(index, image_list):
    if index < 0 or index >= len(image_list):
        return None
    path = os.path.join(INPUT_IMAGE_FOLDER, image_list[index])
    return Image.open(path), path


def get_total_images():
    return len(load_images_from_folder())