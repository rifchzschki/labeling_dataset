from ultralytics import YOLO

# Load a model
model = YOLO("../model/yolo8n-300epochs-v2.pt")  # load a custom model

# Validate the model
metrics = model.val()  # no arguments needed, dataset and settings remembered
metrics.box.map  # map50-95