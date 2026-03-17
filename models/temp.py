from ultralytics import YOLO

model = YOLO("cap_detection.pt")
print(model.names)