import numpy as np
import os
import numpy as np
import pyboof as pb

pb.__init_memmap() #Optional

class QR_Extractor:
    # Src: github.com/lessthanoptimal/PyBoof/blob/master/examples/qrcode_detect.py
    def __init__(self):
        self.detector = pb.FactoryFiducial(np.uint8).qrcode()
    
    def extract(self, img_path):
        if not os.path.isfile(img_path):
            print('File not found:', img_path)
            return None
        image = pb.load_single_band(img_path, np.uint8)
        self.detector.detect(image)
        qr_codes = []
        for qr in self.detector.detections:
            qr_codes.append({
                'text': qr.message,
                'points': qr.bounds.convert_tuple()
            })
        return qr_codes
    
def extract_text_from_image(image_path):
    qr_extractor = QR_Extractor()
    qr_codes = qr_extractor.extract(image_path)
    if qr_codes is None:
        return []
    return qr_codes[0]['text']