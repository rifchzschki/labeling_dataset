import cv2
import numpy as np
from matplotlib import pyplot as plt
import cv2

class Preprocessing:
    def __init__(self, image):
        self.image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def remove_watermark_fft(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        f = np.fft.fft2(gray)
        fshift = np.fft.fftshift(f)
        rows, cols = gray.shape
        crow, ccol = rows // 2, cols // 2
        mask = np.ones((rows, cols), np.uint8)
        mask[crow-30:crow+30, ccol-30:ccol+30] = 0
        fshift = fshift * mask
        f_ishift = np.fft.ifftshift(fshift)
        img_back = np.fft.ifft2(f_ishift)
        img_back = np.abs(img_back)
        return img_back

    def upscale_image(self, image, scale_factor, interpolation=cv2.INTER_CUBIC):
        height, width = image.shape[:2]
        new_size = (int(width * scale_factor), int(height * scale_factor))
        return cv2.resize(image, new_size, interpolation=interpolation)

    def post_process_fft(self, fft_image):
        normalized = cv2.normalize(fft_image, None, 0, 255, cv2.NORM_MINMAX)
        uint8_image = normalized.astype(np.uint8)
        _, binary = cv2.threshold(uint8_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        kernel = np.ones((3,3), np.uint8)
        binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        return binary

    def run(self):
        scale_factor = 2.0
        upscaled_image = self.upscale_image(self.image, scale_factor)
        fft_result = self.remove_watermark_fft(upscaled_image)
        binary_result = self.post_process_fft(fft_result)
        return binary_result
