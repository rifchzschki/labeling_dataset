import cv2, os, numpy as np, random
from ultralytics import YOLO
from utils import getBound

class YOLORunner:
    def __init__(self):
        print('Loading YOLOv8 model...')
        self.model = YOLO(f'../model/yolov8n-300epochs.pt')
        self.input_path = '../data/input/'
        self.output_path = '../data/output/'
        self.masks = None
        self.box = None

    def getCornerPoints(self, image_path):
        image = cv2.imread(image_path)
        results = self.model(image)[0]
        self.masks = results.masks.xy
        self.box = results.boxes

        corner_points = getBound(self.masks[0])

        return corner_points
    
    def draw(self, image_path, corner_points : list[tuple[float, float]]):
        image = cv2.imread(image_path)

        # Color for the class (BGR format)
        color = random.choices(range(256), k=3)

        # Opacity level
        opacity = 0.5

        for mask, box in zip(self.masks, self.box):
            points = np.int32([mask])
            
            # Create a copy of the image to draw the polygon on
            overlay = image.copy()
            
            # Draw the filled polygon on the overlay
            cv2.fillPoly(overlay, points, color)
            
            # Blend the overlay with the original image
            cv2.addWeighted(overlay, opacity, image, 1 - opacity, 0, image)
        
        # Draw the bounding box
        print(corner_points)
        for i in range(4):
            cv2.circle(image, (int(corner_points[i][0]), int(corner_points[i][1])), 30, (0, 0, 255), 20)
        
        return image
    
    def saveImage(self, image_path):
        corner_points = self.getCornerPoints(self.input_path + image_path)

        # Draw and save the image
        cv2.imwrite(self.output_path + image_path, self.draw(self.input_path + image_path, corner_points))
    
    def run(self):
        for image_path in os.listdir(self.input_path):
            print(f'Processing {image_path}...')
            self.saveImage(image_path)

if __name__ == '__main__':
    runner = YOLORunner()
    runner.run()