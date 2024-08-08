import cv2, numpy as np, random
from ultralytics import YOLO

class Segmentation:
    def __init__(self, image_name, image, isInvers=False):
        self.model = YOLO('../../model/yolo8n-300epochs-v2.pt')
        self.image_name = image_name
        self.masks = None
        self.box = None
        self.current_image = image
        self.image_input_path = '../../data/input/' + image_name
        self.output_path_perspective_corrected = '../../data/output/' + image_name
        self.tmp_path = '../../data/tmp/' + image_name
        self.output_path_segmentation = '../../data/output_segmentation/' + image_name
        self.isInvers = isInvers
    
    def getCornerPoints(self):
        # image = self.current_image
        image = cv2.imread(self.image_input_path)
        results = self.model(image)[0]

        if len(results) == 0:
            return []
        
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

        if(self.isInvers):
            for i in range(len(best_quad)):
                best_quad[i][0] = best_quad[i][0]*2
                best_quad[i][1] = best_quad[i][1]*2

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
        
        if len(corner_points) == 0:
            return image
        
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
    
    def processImage(self):
        corner_points = self.getCornerPoints()

        # Draw and save the image
        cv2.imwrite(self.output_path_segmentation, self.draw(corner_points))
        self.current_image = self.correctPerspective(corner_points) if len(corner_points) else self.current_image
        cv2.imwrite(self.output_path_perspective_corrected, self.current_image)
    
    def run(self):
        # current_time = time.time()
        print(f'Segment {self.image_name}...')
        self.processImage()
        # cv2.imshow("uhuy", self.current_image)
        # cv2.waitKey(0)
        return self.current_image
        # print(f'\n\nProcessing finished in {time.time() - current_time} seconds')
