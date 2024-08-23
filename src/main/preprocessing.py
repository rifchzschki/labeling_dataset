import cv2
import numpy as np
from matplotlib import pyplot as plt
import cv2

class Preprocessing:
    def __init__(self, image):
        self.image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def combined_niblack_sauvola(self, image, window_size=15, k=0.2, R=128):
        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        padding = window_size // 2
        padded = cv2.copyMakeBorder(image, padding, padding, padding, padding, cv2.BORDER_REPLICATE)

        integral = cv2.integral(padded.astype(np.float32))
        integral_sq = cv2.integral((padded.astype(np.float32))**2)

        height, width = image.shape

        output = np.zeros_like(image)

        for y in range(height):
            for x in range(width):
                y1, y2, x1, x2 = y, y + window_size, x, x + window_size
                count = window_size * window_size
                sum_val = integral[y2, x2] - integral[y1, x2] - integral[y2, x1] + integral[y1, x1]
                sum_sq = integral_sq[y2, x2] - integral_sq[y1, x2] - integral_sq[y2, x1] + integral_sq[y1, x1]

                mean = sum_val / count
                var = (sum_sq / count) - (mean ** 2)
                std_dev = np.sqrt(var) if var > 0 else 0

                t_niblack = mean + k * std_dev

                t_sauvola = mean * (1 + k * ((std_dev / R) - 1))

                t_combined = (t_niblack + t_sauvola) / 2

                output[y, x] = 0 if padded[y+padding, x+padding] <= t_combined else 255

        return output

    def run(self):
        return self.combined_niblack_sauvola(self.image, window_size=15, k=0.2, R=128)
