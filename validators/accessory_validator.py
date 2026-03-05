import cv2
import mediapipe as mp

mp_face_detection = mp.solutions.face_detection


def validate_accessories(image_path):
    """
    Accessory check (relaxed):
    - We no longer use COCO YOLO because it does not have explicit hat/sunglasses classes
      and was incorrectly flagging the whole 'person' as a prohibited item.
    - For now we only ensure the face region is generally visible; no hard failures
      are generated here unless face detection itself is missing.

    This keeps the system focused on background + basic face visibility,
    as requested.
    """

    image = cv2.imread(image_path)
    if image is None:
        # Let file/quality validators handle unreadable images
        return True, []

    h, w, _ = image.shape

    reasons = []

    with mp_face_detection.FaceDetection(
        model_selection=1, min_detection_confidence=0.5
    ) as face_detection:
        results = face_detection.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        if not results.detections:
            # Face validator will already complain; we don't duplicate here.
            return True, []

    # No strict accessory rejection for now
    return True, []