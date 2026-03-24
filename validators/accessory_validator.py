import cv2
import os
from config.settings import (
    CAP_CONFIDENCE,
    SUNGLASS_CONFIDENCE,
    CAP_MODEL_PATH,
    SUNGLASS_MODEL_PATH
)

from ultralytics import YOLO


cap_model = None
sunglass_model = None

# Load cap model
if os.path.exists(CAP_MODEL_PATH):
    try:
        cap_model = YOLO(CAP_MODEL_PATH)
    except Exception:
        cap_model = None

# Load sunglasses model
if os.path.exists(SUNGLASS_MODEL_PATH):
    try:
        sunglass_model = YOLO(SUNGLASS_MODEL_PATH)
    except Exception:
        sunglass_model = None


def _detect_cap(image):
    if cap_model is None:
        return False

    try:
        results = cap_model.predict(
            source=image,
            verbose=False,
            conf=CAP_CONFIDENCE
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
            if confidence >= CAP_CONFIDENCE and int(class_id) == 0:
                return True

    return False


def _detect_sunglasses(image):
    if sunglass_model is None:
        return False

    try:
        results = sunglass_model.predict(
            source=image,
            verbose=False,
            conf=SUNGLASS_CONFIDENCE
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
            if confidence >= SUNGLASS_CONFIDENCE and int(class_id) == 0:
                return True

    return False


def validate_accessories(image_path):
    image = cv2.imread(image_path)

    if image is None:
        return True, []

    # Check sunglasses first to avoid misclassification as cap
    if _detect_sunglasses(image):
        return False, ["Sunglasses detected"]

    # Then check cap
    if _detect_cap(image):
        return False, ["Cap detected"]

    return True, []