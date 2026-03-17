import cv2
import mediapipe as mp

mp_face_detection = mp.solutions.face_detection


def validate_face(image_path):
    image = cv2.imread(image_path)
    if image is None:
        return False, ["Could not read image for face check"]

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:
        results = face_detection.process(image_rgb)

        if not results.detections:
            return False, ["No face detected"]

        if len(results.detections) > 1:
            return False, ["Multiple faces detected"]

    return True, []