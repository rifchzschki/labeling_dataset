import cv2
from ultralytics import YOLO
from drawDots import draw
from utils import getBound

def run(image_path):
    model = YOLO(f'../model/best.pt')
    image = cv2.imread(image_path)
    results = model(image)[0]
    masks = results.masks.xy

    _, corner_points = getBound(masks[0])

    draw(image_path, corner_points)