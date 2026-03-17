# import cv2

# from config.settings import (
#     ACCESSORY_MODEL_CONFIDENCE,
#     OBJECT_DETECTION_MODEL,
# )


# def _detect_cap(image):

#     if OBJECT_DETECTION_MODEL is None:
#         return False

#     try:
#         results = OBJECT_DETECTION_MODEL.predict(
#             source=image,
#             verbose=False,
#             conf=ACCESSORY_MODEL_CONFIDENCE
#         )
#     except Exception:
#         return False

#     for result in results:
#         boxes = getattr(result, "boxes", None)

#         if boxes is None or boxes.cls is None:
#             continue

#         class_ids = boxes.cls.tolist()
#         confidences = boxes.conf.tolist() if boxes.conf is not None else []

#         for index, class_id in enumerate(class_ids):

#             confidence = confidences[index] if index < len(confidences) else 0.0

#             if confidence < ACCESSORY_MODEL_CONFIDENCE:
#                 continue

#             if int(class_id) == 0:  # class 0 = cap
#                 return True

#     return False


# def validate_accessories(image_path):

#     image = cv2.imread(image_path)

#     if image is None:
#         return True, []

#     cap_detected = _detect_cap(image)

#     if cap_detected:
#         return False, ["Cap detected"]

#     return True, []



import cv2
import os
from config.settings import ACCESSORY_MODEL_CONFIDENCE, CAP_MODEL_PATH

model = None
if os.path.exists(CAP_MODEL_PATH):
    try:
        from ultralytics import YOLO
        model = YOLO(CAP_MODEL_PATH)
    except Exception:
        model = None


def _detect_cap(image):
    if model is None:
        return False

    try:
        results = model.predict(
            source=image,
            verbose=False,
            conf=ACCESSORY_MODEL_CONFIDENCE
        )
    except Exception:
        return False

    for result in results:
        boxes = getattr(result, "boxes", None)
        if boxes is None or boxes.cls is None:
            continue

        class_ids = boxes.cls.tolist()
        confidences = boxes.conf.tolist() if boxes.conf is not None else []

        for index, class_id in enumerate(class_ids):
            confidence = confidences[index] if index < len(confidences) else 0.0
            if confidence >= ACCESSORY_MODEL_CONFIDENCE and int(class_id) == 0:
                return True

    return False


def validate_accessories(image_path):
    image = cv2.imread(image_path)

    if image is None:
        return True, []

    return (False, ["Cap detected"]) if _detect_cap(image) else (True, [])