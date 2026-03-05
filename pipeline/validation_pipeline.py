from validators.file_validator import validate_file
from validators.quality_validator import validate_image_quality
from validators.face_validator import validate_face
from validators.pose_validator import validate_head_pose
from validators.background_validator import validate_background
from validators.accessory_validator import validate_accessories


def run_validation(image_path):

    reasons: list[str] = []
    metrics: dict = {}

    def _normalize_result(result, validator_name: str):
        """
        Backward-compatible unpacking:
        - (bool, [reasons])
        - (bool, [reasons], {metrics})
        """
        try:
            ok, msgs, m = result
        except ValueError:
            ok, msgs = result
            m = {}

        if not isinstance(msgs, list):
            msgs = [str(msgs)]

        if isinstance(m, dict) and m:
            metrics[validator_name] = m

        return bool(ok), msgs

    valid, msg = _normalize_result(validate_file(image_path), "file")
    if not valid:
        reasons.extend(msg)

    # If file is corrupted/unreadable, downstream checks will crash.
    if "Corrupted or unreadable image" in reasons:
        return {"status": "Invalid", "reasons": reasons, "metrics": metrics}

    valid, msg = _normalize_result(validate_image_quality(image_path), "quality")
    if not valid:
        reasons.extend(msg)

    valid, msg = _normalize_result(validate_face(image_path), "face")
    if not valid:
        reasons.extend(msg)

    valid, msg = _normalize_result(validate_head_pose(image_path), "pose")
    if not valid:
        reasons.extend(msg)

    valid, msg = _normalize_result(validate_background(image_path), "background")
    if not valid:
        reasons.extend(msg)

    valid, msg = _normalize_result(validate_accessories(image_path), "accessories")
    if not valid:
        reasons.extend(msg)

    if reasons:
        return {"status": "Invalid", "reasons": reasons, "metrics": metrics}

    return {"status": "Valid", "reasons": [], "metrics": metrics}