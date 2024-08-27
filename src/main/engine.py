from PIL import Image
from paddleocr import PaddleOCR, draw_ocr
import matplotlib.pyplot as plt, os, argparse, cv2
from utils import get_horizontal, crop_image


class Engine:
    def __init__(self, image, text):
        self.image = image
        self.output_path = text
    def run(self):
        ocr  = PaddleOCR(
            lang='en',
            use_gpu=False,
            rec_path=None,
            det_db_thresh=0.5,
            rec_thresh=0.5,
            image_shape=(640, 640),
            use_angle_cls = True,
            )
        
       
        image = cv2.imread(self.image)

        # lakukan teks detection kemudian cari lebar paling panjang
        result_box= ocr.ocr(image, det=True, rec=False, cls=False)
        longest_box_map = get_horizontal(result_box[0])
        # longest_box, is_horizontal = get_horizontal(result_box[0])

        highest_prec = 0
        last_rotate_90 = None
        last_rotate_180 = None
        print(longest_box_map)
        for longest_box, is_horizontal in (longest_box_map):
            rotate_90 = False
            rotate_180 = False
            # crop box dengan lebar paling panjang
            cropped = crop_image(image, longest_box)
            # cv2.imshow("cropped", cropped)
            # cv2.waitKey(0)
            
            # cek tinggi atau lebar box yang paling panjang dan buat gambar menjadi lebar>tinggi (box)
            if(not is_horizontal):
                cropped = cv2.rotate(cropped, cv2.ROTATE_90_CLOCKWISE)
                rotate_90=True
            
            # lakukan 2x recognize ke hasil crop tersebut (normal dan dibalik 180)
            result1= ocr.ocr(cropped, det=False, rec=True, cls=False)
            print("ini result:",result1)
            cropped_tmp = cv2.rotate(cropped, cv2.ROTATE_180)
            result2= ocr.ocr(cropped_tmp, det=False, rec=True, cls=False)
            print("ini result:",result2)
            
            # hasil terbaik akan menjadi direction sebenarnya
            if(result1[0][0][1]<result2[0][0][1]):
                if(result2[0][0][1]>highest_prec):
                    rotate_180=True
                    highest_prec = max(result2[0][0][1], highest_prec)
                    last_rotate_180 = rotate_180
                    last_rotate_90 = rotate_90
            else:
                if(result1[0][0][1]>highest_prec):
                    last_rotate_180 = rotate_180
                    last_rotate_90 = rotate_90
                    highest_prec = max(result1[0][0][1], highest_prec)

        if(last_rotate_90): image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        if(last_rotate_180): image = cv2.rotate(image, cv2.ROTATE_180)

        
        
        # lakukan det, rec untuk mendapatkan hasil ocr
        cv2.imwrite(self.image, image)

        result= ocr.ocr(self.image, det=True, rec=True, cls=False)
        # print(result)

        txts = [line[1][0] for line in result[0]]
        # boxes = [line[0] for line in result[0]]
        # scores = [line[1][1] for line in result[0]]

        # im_show = draw_ocr(self.image, boxes, txts, scores, font_path='Oswald-ExtraLight.ttf')
        # plt.figure(figsize=(15, 8))
        # plt.imshow(im_show)
        # plt.show()
        # print(txts)


        with open(self.output_path, 'w') as f1:
            for(txt) in txts:
                f1.write(txt)
                f1.write("\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="OCR")
    parser.add_argument("arg1", type=str, help="Path gambar")
    parser.add_argument("arg2", type=str, help="Path output")
    args = parser.parse_args()
    Engine(args.arg1, args.arg2).run()