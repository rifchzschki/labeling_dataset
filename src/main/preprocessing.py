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

    def run(self):
        self.filter_black()
        return self.image
