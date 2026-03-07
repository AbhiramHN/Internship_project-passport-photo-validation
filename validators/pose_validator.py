import cv2
import mediapipe as mp
import numpy as np

mp_face_mesh = mp.solutions.face_mesh


def validate_head_pose(image_path):
    """
    Head pose validation:
    - Head must not be tilted
    - Face must be looking straight (nose centred)
    - Fixed bug: return False, reasons (was missing list wrap)
    - Added None guard
    """
    reasons = []

    image = cv2.imread(image_path)
    if image is None:
        return False, ["Could not read image for pose check"]

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    with mp_face_mesh.FaceMesh(static_image_mode=True) as face_mesh:
        results = face_mesh.process(image_rgb)

        if not results.multi_face_landmarks:
            return False, ["Face landmarks not detected"]

        face_landmarks = results.multi_face_landmarks[0]

        left_eye = face_landmarks.landmark[33]
        right_eye = face_landmarks.landmark[263]

        eye_slope = abs(left_eye.y - right_eye.y)

        if eye_slope > 0.03:
            reasons.append("Head tilted - please face the camera straight")

        nose = face_landmarks.landmark[1]

        if nose.x < 0.3 or nose.x > 0.7:
            reasons.append("Face not looking straight ahead")

    if len(reasons) == 0:
        return True, []

    return False, reasons  # ← was missing the list, now correctly returns list