
from paddleocr import PaddleOCR, draw_ocr
from PIL import Image
import matplotlib.pyplot as plt

def run(img, text):
    ocr  = PaddleOCR(
        lang='en',
        use_gpu=False,
        rec_path=None,
        det_db_thresh=0.5,
        rec_thresh=0.5,
        image_shape=(640, 640)
        )
    
    result= ocr.ocr(img, det=True, rec=True)

    txts = [line[1][0] for line in result[0]]
    # boxes = [line[0] for line in result[0]]
    # scores = [line[1][1] for line in result[0]]

    # im_show = draw_ocr(image, boxes, txts, scores, font_path='Oswald-ExtraLight.ttf')
    # plt.figure(figsize=(15, 8))
    # plt.imshow(im_show)
    # plt.show()
    print(txts)


    with open(text, 'w') as f1:
        for(txt) in txts:
            f1.write(txt)
            f1.write("\n")

