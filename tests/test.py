

import unittest
import os
import cv2
from qrdet import QRDetector
from qrcode import qrcodes

current_dir = os.path.dirname(os.path.abspath(__file__))

class TestQRCodeRecognition(unittest.TestCase):
    def test_qr_code_recognition(self):
        data_path = os.path.join(current_dir, 'data')

        filenames = os.listdir(data_path)

        detector = QRDetector(model_size='s')
        for filename in filenames:
            img = cv2.imread(os.path.join(data_path, filename))
            code = qrcodes.detect_qrcode(detector, img)
            print(f'{filename}: {code}')
            self.assertIsNotNone(code)
            pass
        pass


if __name__ == '__main__':
    unittest.main()
    pass