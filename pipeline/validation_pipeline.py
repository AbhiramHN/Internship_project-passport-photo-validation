from validators.file_validator import validate_file
from validators.quality_validator import validate_image_quality
from validators.face_validator import validate_face
from validators.pose_validator import validate_head_pose
from validators.background_validator import validate_background
from validators.accessory_validator import validate_accessories


def run_validation(image_path):

    reasons: list[str] = []
    metrics: dict = {}
    validation_flow: list[str] = []

    def _normalize_result(result, validator_name: str):
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
    validation_flow.append(
        "file_validator.py validated the photo" if valid
        else "file_validator.py invalidated the photo"
    )
    if not valid:
        reasons.extend(msg)

    if "Corrupted or unreadable image" in reasons:
        return {
            "status": "Invalid",
            "reasons": reasons,
            "metrics": metrics,
            "flow": validation_flow
        }

    valid, msg = _normalize_result(validate_image_quality(image_path), "quality")
    validation_flow.append(
        "quality_validator.py validated the photo" if valid
        else "quality_validator.py invalidated the photo"
    )
    if not valid:
        reasons.extend(msg)

    valid, msg = _normalize_result(validate_face(image_path), "face")
    validation_flow.append(
        "face_validator.py validated the photo" if valid
        else "face_validator.py invalidated the photo"
    )
    if not valid:
        reasons.extend(msg)

    valid, msg = _normalize_result(validate_head_pose(image_path), "pose")
    validation_flow.append(
        "pose_validator.py validated the photo" if valid
        else "pose_validator.py invalidated the photo"
    )
    if not valid:
        reasons.extend(msg)

    valid, msg = _normalize_result(validate_background(image_path), "background")
    validation_flow.append(
        "background_validator.py validated the photo" if valid
        else "background_validator.py invalidated the photo"
    )
    if not valid:
        reasons.extend(msg)

    valid, msg = _normalize_result(validate_accessories(image_path), "accessories")
    validation_flow.append(
        "accessory_validator.py validated the photo" if valid
        else "accessory_validator.py invalidated the photo"
    )
    if not valid:
        reasons.extend(msg)

    if reasons:
        return {
            "status": "Invalid",
            "reasons": reasons,
            "metrics": metrics,
            "flow": validation_flow
        }

    return {
        "status": "Valid",
        "reasons": [],
        "metrics": metrics,
        "flow": validation_flow
    }