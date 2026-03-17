# import os

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ALLOWED_FORMATS = ["jpg", "jpeg", "png"]

# MAX_FILE_SIZE_KB = 300

# ASPECT_RATIO_MIN = 0.65
# ASPECT_RATIO_MAX = 0.75

# MIN_RESOLUTION_WIDTH = 300
# MIN_RESOLUTION_HEIGHT = 400

# BLUR_THRESHOLD = 100

# FACE_DETECTION_MODEL = "retinaface"

# BACKGROUND_VARIANCE_THRESHOLD = 15

# INPUT_IMAGE_FOLDER = os.path.join(BASE_DIR, "data", "input_images")
# UPLOAD_FOLDER = os.path.join(BASE_DIR, "data", "uploaded_images")
# ACCEPTED_FOLDER = os.path.join(BASE_DIR, "data", "accepted")
# REJECTED_FOLDER = os.path.join(BASE_DIR, "data", "rejected")

# ACCESSORY_MODEL_CONFIDENCE = 0.60

# CAP_MODEL_PATH = os.path.join(BASE_DIR, "models", "cap_detection.pt")

# OBJECT_DETECTION_MODEL = None

# if os.path.exists(CAP_MODEL_PATH):
#     try:
#         from ultralytics import YOLO
#         OBJECT_DETECTION_MODEL = YOLO(CAP_MODEL_PATH)
#     except Exception:
#         OBJECT_DETECTION_MODEL = None



import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ALLOWED_FORMATS = ["jpg", "jpeg", "png"]

MAX_FILE_SIZE_KB = 300

ASPECT_RATIO_MIN = 0.65
ASPECT_RATIO_MAX = 0.75

MIN_RESOLUTION_WIDTH = 300
MIN_RESOLUTION_HEIGHT = 400

BLUR_THRESHOLD = 100

FACE_DETECTION_MODEL = "retinaface"

BACKGROUND_VARIANCE_THRESHOLD = 15

INPUT_IMAGE_FOLDER = os.path.join(BASE_DIR, "data", "input_images")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "data", "uploaded_images")
ACCEPTED_FOLDER = os.path.join(BASE_DIR, "data", "accepted")
REJECTED_FOLDER = os.path.join(BASE_DIR, "data", "rejected")

ACCESSORY_MODEL_CONFIDENCE = 0.60

CAP_MODEL_PATH = os.path.join(BASE_DIR, "models", "cap_detection.pt")