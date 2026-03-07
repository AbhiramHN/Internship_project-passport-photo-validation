import cv2
from config.settings import BLUR_THRESHOLD


def validate_image_quality(image_path):
    """
    Image quality checks:
    - Blur detection using Laplacian variance
    - Added None guard for unreadable images
    """
    reasons = []

    image = cv2.imread(image_path)
    if image is None:
        return False, ["Could not read image for quality check"]

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()

    if laplacian_var < BLUR_THRESHOLD:
        reasons.append("Image is blurred")

    if len(reasons) == 0:
        return True, []

    return False, reasons