from qrdet import QRDetector
import cv2
import os
from scipy import ndimage
import pyzbar.pyzbar
from PIL import Image

class MoliQRCodeDecoder:
    def __init__(self, ):
        self.detector = QRDetector(model_size='s')
        current_path = os.path.dirname(os.path.abspath(__file__))
        self.decoder_wechat = cv2.wechat_qrcode_WeChatQRCode(
            os.path.join(current_path, "detect.prototxt"), 
            os.path.join(current_path, "detect.caffemodel"), 
            os.path.join(current_path, "sr.prototxt"), 
            os.path.join(current_path, "sr.caffemodel"))
        
        self.decode_functions = [self.decode_wechat, self.decode_zabar]
        pass

    def decode_zabar(self, img):
        qr_code = pyzbar.pyzbar.decode(Image.fromarray(img))
        if not qr_code:
            return None
        return qr_code[0].data.decode('utf-8')
        pass

    def decode_wechat(self, img):
        qr_code, points = self.decoder_wechat.detectAndDecode(img)
        if not qr_code:
            return None
        else:
            return qr_code[0]

    def transform_image(self, image):
        yield image

        for i in range(3):
            image[:, :, i] = cv2.equalizeHist(image[:, :, i])
            yield image

        pass

    def detectAndDecode(self, image):
        detections = self.detector.detect(image=image, is_bgr=True)

        if not detections:
            print('No QR code detected')
            return None
        
        # print(len(detections))
        detection = detections[0]
        # print(detection)
        x1, y1, x2, y2 = detection['bbox_xyxy']

        x1 = int(x1)
        y1 = int(y1)
        x2 = int(x2)
        y2 = int(y2)

        x11 = x1 - 2
        y11 = y1 - 2
        x22 = x2 + 2
        y22 = y2 + 2

        img = image[y11:y22, x11:x22]
        # normalize contrast

        for img in self.transform_image(img):
            img = cv2.GaussianBlur(img, (3, 3), 0)
            for d in range(-180, 180, 30):
                img_ = ndimage.rotate(img, d)
                
                for decode_function in self.decode_functions:
                    qr_code = decode_function(img_)
                    if qr_code:
                        return qr_code
                    else:
                        continue 
                    pass
                pass
            pass

        return None  