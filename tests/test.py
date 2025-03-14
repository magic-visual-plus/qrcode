

import unittest
import os
import cv2
from moli_qrcode import moli_qrcode_decoder

current_dir = os.path.dirname(os.path.abspath(__file__))

class TestQRCodeRecognition(unittest.TestCase):
    def test_qr_code_recognition(self):
        data_path = os.path.join(current_dir, 'data')

        filenames = os.listdir(data_path)

        filenames = [f for f in filenames if f.endswith('.jpg') or f.endswith('.png')]
        
        decoder = moli_qrcode_decoder.MoliQRCodeDecoder()
        for filename in filenames:
            img = cv2.imread(os.path.join(data_path, filename))
            code = decoder.detectAndDecode(img)
            print(f'{filename}: {code}')
            self.assertIsNotNone(code)
            pass
        pass


if __name__ == '__main__':
    unittest.main()
    pass