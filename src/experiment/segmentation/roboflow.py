from inference_sdk import InferenceHTTPClient
import numpy as np
from main.utils import getBound
from drawDots import draw

def run(image_path):
    CLIENT = InferenceHTTPClient(
    api_url="https://outline.roboflow.com",
    api_key="o9GwcWEFBZ1Fk1R5MRt7"
    )

    result = CLIENT.infer(image_path, model_id="document-segmentation-j6olp/1")
    predictions = result['predictions']
    points = predictions[0]['points']
    points_np = np.array([[p['x'], p['y']] for p in points], dtype=np.float32)
    _ , corner_coordinates = getBound(points_np)
    draw(image_path, corner_coordinates)