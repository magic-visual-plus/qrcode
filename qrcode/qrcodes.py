from qrdet import QRDetector
import cv2
import sys
import pyzbar.pyzbar
from PIL import Image
import sys
import os
import numpy as np
from scipy import ndimage


def detect_qrcode(detector, image):
    detections = detector.detect(image=image, is_bgr=True)

    if not detections:
        print('No QR code detected')
        return None
    
    # print(len(detections))
    detection = detections[0]
    # print(detection)
    x1, y1, x2, y2 = detection['bbox_xyxy']

    x1 = int(x1) - 2
    y1 = int(y1) - 2
    x2 = int(x2) + 2 
    y2 = int(y2) + 2

    img = image[y1:y2, x1:x2]
    img = cv2.GaussianBlur(img, (3, 3), 0)

    for d in range(-180, 180, 30):
        img_ = ndimage.rotate(img, d)
        qr_code = pyzbar.pyzbar.decode(Image.fromarray(img_))

        if not qr_code:
            # print(f'QR code: {qr_code[0].data.decode("utf-8")}')
            continue
        else:
            return qr_code[0].data.decode('utf-8')
        pass

    return None
    pass

if __name__ == '__main__':
    detector = QRDetector(model_size='s')
    input_path = sys.argv[1]
    
    img = cv2.imread(input_path)
    qr_code = detect_qrcode(detector, img)
    print(f'QR code: {qr_code}')
    pass