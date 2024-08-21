import cv2
import numpy as np
from matplotlib import pyplot as plt
import cv2

class Preprocessing:
    def __init__(self, image):
        self.image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def sauvola_threshold(self, image, window_size=15, k=0.2, R=128):
        height, width = image.shape
        padding = window_size // 2
        padded = cv2.copyMakeBorder(image, padding, padding, padding, padding, cv2.BORDER_REFLECT)

        integral_img = cv2.integral(padded.astype(np.float32))
        integral_sqimg = cv2.integral((padded.astype(np.float32))**2)

        output = np.zeros_like(image)

        for y in range(height):
            for x in range(width):
                y1, x1 = y, x
                y2, x2 = y + window_size, x + window_size

                count = window_size**2
                sum_value = integral_img[y2, x2] - integral_img[y1, x2] - integral_img[y2, x1] + integral_img[y1, x1]
                sum_sq = integral_sqimg[y2, x2] - integral_sqimg[y1, x2] - integral_sqimg[y2, x1] + integral_sqimg[y1, x1]

                mean = sum_value / count
                std_dev = np.sqrt((sum_sq / count) - (mean**2))

                threshold = mean * (1 + k * ((std_dev / R) - 1))
                output[y, x] = 255 if padded[y+padding, x+padding] > threshold else 0

        return output

    def upscale_image(self, image, scale_factor, interpolation=cv2.INTER_CUBIC):
        height, width = image.shape[:2]
        new_size = (int(width * scale_factor), int(height * scale_factor))
        return cv2.resize(image, new_size, interpolation=interpolation)

    def combine_thresholds(self, nick_thresh, otsu_thresh):
        combined = cv2.bitwise_and(nick_thresh, otsu_thresh)

        kernel = np.ones((3,3), np.uint8)
        dilated = cv2.dilate(combined, kernel, iterations=1)

        final = cv2.bitwise_or(combined, dilated)

        return final

    def run(self):
        scale_factor = 2.0
        upscaled_image = self.upscale_image(self.image, scale_factor)

        sauvola_thresholded = self.sauvola_threshold(upscaled_image)

        _, otsu_thresholded = cv2.threshold(upscaled_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        combined_threshold = self.combine_thresholds(sauvola_thresholded, otsu_thresholded)
        
        return combined_threshold
