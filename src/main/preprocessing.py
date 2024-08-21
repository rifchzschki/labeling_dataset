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

    def run(self):
        scale_factor = 2.0
        upscaled_image = self.upscale_image(self.image, scale_factor)
        res = self.remove_watermark_fft(upscaled_image)*(-1)
        
        return res
