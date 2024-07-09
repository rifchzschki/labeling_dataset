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
        self.current_image = None

    def getCornerPoints(self, image_path):
        image = cv2.imread(image_path)
        results = self.model(image)[0]
        self.masks = results.masks.xy
        self.box = results.boxes

        corner_points = getBound(self.masks[0])

        return corner_points
    
    def draw(self, image_path, corner_points : list[tuple[float, float]]):
        image = self.current_image

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
        
        for i in range(4):
            cv2.circle(image, (int(corner_points[i][0]), int(corner_points[i][1])), 30, (0, 0, 255), 20)
        
        return image

    def correctPerspective(self, image, points):
        r= np.zeros((4,2), dtype="float32")
        s = np.sum(points, axis=1);r[0] = points[np.argmin(s)];r[2] = points[np.argmax(s)]
        d = np.diff(points, axis=1);r[1] = points[np.argmin(d)];r[3] = points[np.argmax(d)]
        (tl, tr, br, bl) =r
        wA = np.sqrt((tl[0]-tr[0])**2 + (tl[1]-tr[1])**2 )
        wB = np.sqrt((bl[0]-br[0])**2 + (bl[1]-br[1])**2 )
        maxW = max(int(wA), int(wB))
        hA = np.sqrt((tl[0]-bl[0])**2 + (tl[1]-bl[1])**2 )
        hB = np.sqrt((tr[0]-br[0])**2 + (tr[1]-br[1])**2 )
        maxH = max(int(hA), int(hB))
        ds= np.array([[0,0],[maxW-1, 0],[maxW-1, maxH-1],[0, maxH-1]], dtype="float32")
        transformMatrix = cv2.getPerspectiveTransform(r,ds)
        scan = cv2.warpPerspective(image, transformMatrix, (maxW, maxH))

        return scan
    
    def filter_black(image_path, output_path):
        # Membaca gambar
        image = cv2.imread(image_path)
        
        # Konversi gambar ke skala abu-abu
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Binarisasi gambar (thresholding)
        # Jika piksel lebih gelap dari threshold tertentu, akan dianggap hitam, sisanya akan menjadi putih
        _, binary_image = cv2.threshold(gray_image, 100, 255, cv2.THRESH_BINARY)
        
        # # Inversi gambar biner untuk membuat latar belakang putih dan objek hitam
        inverted_image = cv2.bitwise_not(binary_image)
        
        # Menyimpan gambar hasil
        cv2.imwrite(output_path, inverted_image)
        
    def saveImage(self, image_path):
        corner_points = self.getCornerPoints(self.input_path + image_path)

        # corredted_image = self.correctPerspective(self.current_image, corner_points)

        # Draw and save the image
        cv2.imwrite(self.output_path + image_path, self.draw(self.input_path + image_path, corner_points))
    
    def run(self):
        for image_path in os.listdir(self.input_path):
            print(f'Processing {image_path}...')
            self.current_image = cv2.imread(self.input_path + image_path)
            self.saveImage(image_path)

if __name__ == '__main__':
    runner = YOLORunner()
    runner.run()