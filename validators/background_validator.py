import cv2
import numpy as np
import mediapipe as mp
from sklearn.cluster import KMeans

mp_selfie_segmentation = mp.solutions.selfie_segmentation


def validate_background(image_path):
    """
    Robust passport background validator.

    Accepts:
    - Plain studio backgrounds
    - Solid colors
    - Slight lighting gradients

    Rejects:
    - Forest / grass / outdoor scenes
    - Rooms / objects
    - Textured walls or curtains
    """

    image = cv2.imread(image_path)
    if image is None:
        return True, []

    h, w, _ = image.shape
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # --- Person segmentation ---
    with mp_selfie_segmentation.SelfieSegmentation(model_selection=1) as segmenter:
        result = segmenter.process(image_rgb)

    mask = result.segmentation_mask
    person_mask = mask > 0.6
    bg_mask = np.logical_not(person_mask)

    bg_pixels = image[bg_mask]

    if len(bg_pixels) < 200:
        return True, []

    # --- Dominant color clustering ---
    pixels = bg_pixels.reshape(-1, 3)

    try:
        kmeans = KMeans(n_clusters=3, n_init=10)
        kmeans.fit(pixels)

        counts = np.bincount(kmeans.labels_)
        dominant_ratio = counts.max() / len(pixels)

    except Exception:
        dominant_ratio = 1.0

    # --- Edge density ---
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 60, 140)

    bg_edges = edges[bg_mask]
    edge_density = np.sum(bg_edges > 0) / max(len(bg_edges), 1)

    # --- Texture detection ---
    lap = cv2.Laplacian(gray, cv2.CV_64F)
    bg_lap = lap[bg_mask]
    texture_score = np.var(bg_lap)

    # --- Signals ---
    complex_color = dominant_ratio < 0.65
    high_edges = edge_density > 0.12
    high_texture = texture_score > 180

    signals = sum([complex_color, high_edges, high_texture])

    # Require at least TWO signals to reject
    if signals >= 2:
        return False, ["Background is not plain (too busy or textured)"]

    return True, []