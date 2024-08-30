import cv2
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:/Users/Acer/AppData/Local/Programs/Tesseract-OCR/tesseract'
img_cv = cv2.imread(r'../data/input/IMG_2002.jpeg')
img_cv2 = cv2.imread(r'../data/output/IMG_2002.jpeg')

# By default OpenCV stores images in BGR format and since pytesseract assumes RGB format,
# we need to convert from BGR to RGB format/mode:
img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
img_rgb2 = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2RGB)
# OR
# img_rgb = Image.frombytes('RGB', img_cv.shape[:2], img_cv, 'raw', 'BGR', 0, 0)
# img_rgb2 = Image.frombytes('RGB', img_cv2.shape[:2], img_cv2, 'raw', 'BGR', 0, 0)
# print("Sebelum")
# print(pytesseract.image_to_string(img_rgb))
# print("Sesudah")
# print(pytesseract.image_to_string(img_rgb2))

with open('Sebelum.txt', 'w') as f1:
    f1.write(pytesseract.image_to_string(img_rgb))
    f1.close()
with open('Sesudah.txt', 'w') as f2:
    f2.write(pytesseract.image_to_string(img_rgb2))
    f2.close()