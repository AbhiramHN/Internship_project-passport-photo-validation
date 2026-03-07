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

ACCESSORY_MODEL = "yolov8n"

BACKGROUND_VARIANCE_THRESHOLD = 15

INPUT_IMAGE_FOLDER = os.path.join(BASE_DIR, "data", "input_images")

UPLOAD_FOLDER = os.path.join(BASE_DIR, "data", "uploaded_images")

ACCEPTED_FOLDER = os.path.join(BASE_DIR, "data", "accepted")

REJECTED_FOLDER = os.path.join(BASE_DIR, "data", "rejected")