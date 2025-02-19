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
    # cv2.imwrite(os.path.join(output_path, filename), img)

    for d in range(-36, 36, 6):
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
    output_path = sys.argv[2]
    
    filenames = os.listdir(input_path)
    for filename in filenames:
        if filename.startswith('.'):
            continue
        image = cv2.imread(os.path.join(input_path, filename))
        qr_code = detect_qrcode(detector, image)

        if qr_code:
            print(f'{filename}: {qr_code}')
            pass
        else:
            print(f'No QR code recognized in {filename}')
            pass
        pass