# from validators.file_validator import validate_file
# from validators.quality_validator import validate_image_quality
# from validators.face_validator import validate_face
# from validators.pose_validator import validate_head_pose
# from validators.background_validator import validate_background
# from validators.accessory_validator import validate_accessories


# def run_validation(image_path):

#     metrics: dict = {}
#     validation_flow: list[str] = []

#     def _normalize_result(result, validator_name: str):
#         try:
#             ok, msgs, m = result
#         except ValueError:
#             ok, msgs = result
#             m = {}

#         if not isinstance(msgs, list):
#             msgs = [str(msgs)]

#         if isinstance(m, dict) and m:
#             metrics[validator_name] = m

#         return bool(ok), msgs

#     validators = [
#         ("file", "file_validator.py", validate_file),
#         ("quality", "quality_validator.py", validate_image_quality),
#         ("face", "face_validator.py", validate_face),
#         ("pose", "pose_validator.py", validate_head_pose),
#         ("background", "background_validator.py", validate_background),
#         ("accessories", "accessory_validator.py", validate_accessories),
#     ]

#     for validator_key, validator_file, validator_func in validators:
#         valid, msg = _normalize_result(validator_func(image_path), validator_key)
#         validation_flow.append(
#             f"{validator_file} validated the photo" if valid
#             else f"{validator_file} invalidated the photo"
#         )

#         if not valid:
#             return {
#                 "status": "Invalid",
#                 "reasons": msg,
#                 "metrics": metrics,
#                 "flow": validation_flow
#             }

#     return {
#         "status": "Valid",
#         "reasons": [],
#         "metrics": metrics,
#         "flow": validation_flow
#     }



from validators.file_validator import validate_file
from validators.quality_validator import validate_image_quality
from validators.face_validator import validate_face
from validators.pose_validator import validate_head_pose
from validators.background_validator import validate_background
from validators.accessory_validator import validate_accessories


def run_validation(image_path):

    metrics: dict = {}
    validation_flow: list[str] = []

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

    for validator_key, validator_func in validators:
        valid, msg = _normalize_result(validator_func(image_path), validator_key)
        label = f"{validator_key}_validator.py"
        validation_flow.append(
            f"{label} validated the photo" if valid
            else f"{label} invalidated the photo"
        )

        if not valid:
            return {
                "status": "Invalid",
                "reasons": msg,
                "metrics": metrics,
                "flow": validation_flow
            }

    return {
        "status": "Valid",
        "reasons": [],
        "metrics": metrics,
        "flow": validation_flow
    }