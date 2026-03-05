import cv2
import numpy as np
import mediapipe as mp

mp_face_detection = mp.solutions.face_detection


def validate_background(image_path):

    image = cv2.imread(image_path)
    if image is None:
        return True, []

    h, w, _ = image.shape

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:

        results = face_detection.process(image_rgb)

        if not results.detections:
            return True, []

        bbox = results.detections[0].location_data.relative_bounding_box

        x = int(bbox.xmin * w)
        y = int(bbox.ymin * h)
        bw = int(bbox.width * w)
        bh = int(bbox.height * h)

        # remove face region
        mask = np.ones((h, w), dtype=np.uint8)
        mask[y:y+bh, x:x+bw] = 0

        background_pixels = image[mask == 1]

        if len(background_pixels) == 0:
            return True, []

        # convert to HSV
        hsv = cv2.cvtColor(background_pixels.reshape(-1,1,3), cv2.COLOR_BGR2HSV)
        hsv = hsv.reshape(-1,3)

        brightness = np.mean(hsv[:, 2])
        saturation = np.mean(hsv[:, 1])
        color_std = np.std(hsv[:, 0])

        # Much more relaxed rules: allow any plain color background.
        # Only reject if it is clearly dark/colored + highly inconsistent
        # (typical of rooms, forests, etc.).
        if brightness < 60:
            return False, ["Background too dark"]

        # High saturation AND high hue variance together usually means busy scene.
        if saturation > 80 and color_std > 40:
            return False, ["Background not plain (too textured/colored)"]

    return True, []