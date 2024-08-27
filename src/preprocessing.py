import cv2
import numpy as np
from matplotlib import pyplot as plt
import cv2

class Preprocessing:
    def __init__(self, image):
        self.image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def filter_black(self):
        # Membaca gambar
        # image = self.image
        
        # Konversi gambar ke skala abu-abu
        gray_image = self.image
        
        # Binarisasi gambar (thresholding)
        # Jika piksel lebih gelap dari threshold tertentu, akan dianggap hitam, sisanya akan menjadi putih
        _, binary_image = cv2.threshold(gray_image, 100, 255, cv2.THRESH_BINARY)
        
        # # Inversi gambar biner untuk membuat latar belakang putih dan objek hitam
        inverted_image = cv2.bitwise_not(binary_image)
        
        self.image = inverted_image

    def high_pass_sharpen(self, image):
        kernel = np.array([[-1, -1, -1],
                        [-1,  9, -1],
                        [-1, -1, -1]])
        sharpened = cv2.filter2D(image, -1, kernel)
        sharpened = np.clip(sharpened, 0, 255).astype(np.uint8)
        return sharpened

    def estimate_blur(self,image):
        return cv2.Laplacian(image, cv2.CV_64F).var()

    def apply_dynamic_blur(self, image, blur_threshold=100):
        blur_level = self.estimate_blur(image)
        ksize = None
        if blur_level < blur_threshold:
            ksize = (13, 13)
        else:
            ksize = (5,5)
        blurred_image = cv2.GaussianBlur(image, ksize, sigmaX=0)
        return blurred_image
    
    def dynamic_threshold(self, image):
        mean_intensity = np.mean(image)
        if mean_intensity > 127:
            block_size = 9
            C = 3
        else:
            block_size = 11
            C = 5
        return cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, block_size, C)
    
    def normalize_image(self, image):
        return cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_32F)

    def remove_pepper_noise(self, image, kernel_size):
        kernel = np.ones(kernel_size, np.uint8)
        opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
        return opening

    def nlm(self, image):
        denoised = cv2.bilateralFilter(image, d=10, sigmaColor=100, sigmaSpace=100)
        blurred = cv2.GaussianBlur(denoised, (3,3), 0)
        sharpened = cv2.addWeighted(denoised, 1.5, blurred, -0.5, 0)
        return sharpened

    def apply_clahe(self, image, clip_limit=2.0, tile_grid_size=(8, 8)):
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
        cl_image = clahe.apply(image)
        return cl_image
    
    def upscale_image(self, image, scale_factor, interpolation=cv2.INTER_CUBIC):
        height, width = image.shape[:2]
        new_size = (int(width * scale_factor), int(height * scale_factor))
        return cv2.resize(image, new_size, interpolation=interpolation)

    def run(self):
        # scale_factor = 2.0
        
        # upscaled_image = self.upscale_image(self.image, scale_factor)

        # denoised_image = self.nlm(upscaled_image)

        # enhanced_image = self.apply_clahe(denoised_image)

        # thresholded_image = self.dynamic_threshold(enhanced_image)

        # filtered_image = self.remove_pepper_noise(thresholded_image, kernel_size=(2, 2))

        # scaled_image = self.normalize_image(filtered_image)
        # cv2.imshow("scal", scaled_image)
        # cv2.waitKey(0)
        # self.filter_black()
        return self.image
        # return scaled_image
