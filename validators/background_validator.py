import cv2
import numpy as np
import mediapipe as mp

mp_selfie_segmentation = mp.solutions.selfie_segmentation


def validate_background(image_path):
    image = cv2.imread(image_path)
    if image is None:
        return True, []

    #  Downscale to reduce noise (important)
    image = cv2.resize(image, (256, 256))

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # --- Person segmentation ---
    with mp_selfie_segmentation.SelfieSegmentation(model_selection=1) as segmenter:
        result = segmenter.process(image_rgb)

    mask = result.segmentation_mask
    person_mask = mask > 0.6
    bg_mask = np.logical_not(person_mask)

    bg_pixels = image[bg_mask]

    if len(bg_pixels) < 300:
        return True, []

    # --- COLOR UNIFORMITY ---
    color_std = np.std(bg_pixels, axis=0).mean()

    # --- HSV ---
    bg_hsv = cv2.cvtColor(bg_pixels.reshape(-1, 1, 3), cv2.COLOR_BGR2HSV).reshape(-1, 3)
    saturation = bg_hsv[:, 1]
    avg_saturation = np.mean(saturation)

    # --- EDGE DENSITY ---
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 80, 160)

    bg_edges = edges[bg_mask]
    edge_density = np.sum(bg_edges > 0) / max(len(bg_edges), 1)

    # --- TEXTURE ---
    lap = cv2.Laplacian(gray, cv2.CV_64F)
    bg_lap = lap[bg_mask]
    texture_score = np.var(bg_lap)


    # Hard fails
    if color_std > 35:
        return False, ["Background is not uniform"]

    if avg_saturation > 70:
        return False, ["Background is too colorful"]

    # Soft signals
    high_edges = edge_density > 0.12
    high_texture = texture_score > 400

    # Combine texture + edges
    if high_edges and high_texture:
        return False, ["Background has texture or patterns"]

    return True, []