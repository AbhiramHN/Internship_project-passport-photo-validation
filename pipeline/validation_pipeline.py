from validators.file_validator import validate_file
from validators.quality_validator import validate_image_quality
from validators.face_validator import validate_face
from validators.pose_validator import validate_head_pose
from validators.background_validator import validate_background
from validators.accessory_validator import validate_accessories


def run_validation(image_path):

    metrics: dict = {}
    validation_flow: list[str] = []
    all_reasons: list[str] = []

    def _normalize_result(result, validator_name: str):
        if len(result) == 3:
            ok, msgs, m = result
        else:
            ok, msgs = result
            m = {}

        if not isinstance(msgs, list):
            msgs = [str(msgs)]

        if isinstance(m, dict) and m:
            metrics[validator_name] = m

        return bool(ok), msgs

    validators = [
        ("file", validate_file),
        ("quality", validate_image_quality),
        ("face", validate_face),
        ("pose", validate_head_pose),
        ("background", validate_background),
        ("accessories", validate_accessories),
    ]

    overall_valid = True

    for validator_key, validator_func in validators:
        valid, msgs = _normalize_result(
            validator_func(image_path),
            validator_key
        )

        label = f"{validator_key}_validator.py"

        if valid:
            validation_flow.append(f"{label} validated the photo")
        else:
            validation_flow.append(f"{label} invalidated the photo")
            overall_valid = False
            all_reasons.extend(msgs)

    return {
        "status": "Valid" if overall_valid else "Invalid",
        "reasons": [] if overall_valid else all_reasons,
        "metrics": metrics,
        "flow": validation_flow
    }