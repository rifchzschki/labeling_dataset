from segmentation import Segmentation
from preprocessing import Preprocessing
import time, argparse

class Main():
    def __init__(self, image_name, image_path, invers=False):
        import cv2
        self.image_path = image_path
        self.image_path_after = '../../data/tmp/' + image_name
        self.image = cv2.imread(self.image_path)

        if(not invers):
            self.seg = Segmentation(image_name, image_path, self.image).run()
            self.prep = Preprocessing(self.seg).run()
            cv2.imwrite(self.image_path_after,self.prep)
        else:
            self.prep = Preprocessing(self.image).run()
            cv2.imwrite(self.image_path_after,self.prep)
            self.seg = Segmentation(image_name, image_path, cv2.imread(self.image_path_after), True).run()
            cv2.imwrite(self.image_path_after,self.seg)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Pre-OCR")
    parser.add_argument("arg1", type=str, help="image_name")
    parser.add_argument("arg2", type=str, help="image_path")
    parser.add_argument("arg3", type=str, help="isInvers")
    args = parser.parse_args()
    if(args.arg3 == "y"):
        Main(args.arg1, args.arg2, True)
    else:
        Main(args.arg1, args.arg2, False)
