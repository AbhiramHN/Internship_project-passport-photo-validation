import os
from PIL import Image
from config.settings import ALLOWED_FORMATS, MAX_FILE_SIZE_KB


def validate_file(image_path):
    reasons: list[str] = []
    metrics: dict = {}

    extension = image_path.split(".")[-1].lower()
    if extension not in ALLOWED_FORMATS:
        reasons.append("Invalid file format (only .jpg/.jpeg/.png allowed)")

    file_size_kb = os.path.getsize(image_path) / 1024
    metrics["file_size_kb"] = round(file_size_kb, 2)
    if file_size_kb > MAX_FILE_SIZE_KB:
        reasons.append("File size exceeds 300 KB")

    try:
        with Image.open(image_path) as img:
            img.verify()
        img = Image.open(image_path)  # reopen after verify() just for metrics
    except Exception:
        reasons.append("Corrupted or unreadable image")
        return False, reasons, metrics

    try:
        width, height = img.size
        metrics["width_px"] = int(width)
        metrics["height_px"] = int(height)

        # NOTE: By user request we do NOT hard-reject on resolution or aspect here.
        # We only compute metrics so they can be displayed in the UI if needed.
        dpi = img.info.get("dpi")
        if isinstance(dpi, tuple) and len(dpi) >= 2 and dpi[0] and dpi[1]:
            xdpi, ydpi = float(dpi[0]), float(dpi[1])
            metrics["dpi"] = (round(xdpi, 2), round(ydpi, 2))
    finally:
        try:
            img.close()
        except Exception:
            pass

    if len(reasons) == 0:
        return True, [], metrics

    return False, reasons, metrics