import cv2, os, numpy as np, random, time
from ultralytics import YOLO
from utils import getBound

class YOLORunner:
    def __init__(self, applyBlackFilter=False):
        print('Loading YOLOv8 model...')
        self.model = YOLO(f'../model/yolo8n-300epochs-v2.pt')
        self.input_path = '../data/input/'
        self.output_path_perspective_corrected = '../data/output/'
        self.output_path_segmentation = '../data/output_segmentation/'
        self.masks = None
        self.box = None
        self.current_image = None
        self.applyBlackFilter = applyBlackFilter

    def getCornerPoints(self):
        image = self.current_image
        results = self.model(image)[0]
        
        self.masks = results.masks.xy
        self.box = results.boxes

        # Menghitung convex hull dari titik-titik
        hull = cv2.convexHull(self.masks[0])
        hull_points = hull.reshape(-1, 2)

        # Mencari kombinasi 4 titik yang membentuk area terbesar
        max_area = 0
        best_quad = None
        n = len(hull_points)

        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    for l in range(k + 1, n):
                        quad = np.array([hull_points[i], hull_points[j], hull_points[k], hull_points[l]])
                        area = cv2.contourArea(quad)
                        if area > max_area:
                            max_area = area
                            best_quad = quad

        return best_quad
    
    def draw(self, corner_points : list[tuple[float, float]]):
        image = self.current_image.copy()

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

    def correctPerspective(self, points):
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
        scan = cv2.warpPerspective(self.current_image, transformMatrix, (maxW, maxH))

        return scan
    
    def filter_black(self):
        # Membaca gambar
        image = self.current_image
        
        # Konversi gambar ke skala abu-abu
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Binarisasi gambar (thresholding)
        # Jika piksel lebih gelap dari threshold tertentu, akan dianggap hitam, sisanya akan menjadi putih
        _, binary_image = cv2.threshold(gray_image, 100, 255, cv2.THRESH_BINARY)
        
        # # Inversi gambar biner untuk membuat latar belakang putih dan objek hitam
        inverted_image = cv2.bitwise_not(binary_image)
        
        self.current_image = inverted_image
        
    def processImage(self, image_path):
        corner_points = self.getCornerPoints()

        # Draw and save the image
        cv2.imwrite(self.output_path_segmentation + image_path, self.draw(corner_points))

        if self.applyBlackFilter:
            self.filter_black()
        
        cv2.imwrite(self.output_path_perspective_corrected + image_path, self.correctPerspective(corner_points))

    
    def run(self):
        current_time = time.time()
        for image_path in os.listdir(self.input_path):
            print(f'Processing {image_path}...')
            self.current_image = cv2.imread(self.input_path + image_path)
            self.processImage(image_path)
        print(f'\n\nProcessing finished in {time.time() - current_time} seconds')

if __name__ == '__main__':
    runner = YOLORunner()
    runner.run()