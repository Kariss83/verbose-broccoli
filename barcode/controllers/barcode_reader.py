import os
import io
import base64
from PIL import Image
import cv2

from pyzbar.pyzbar import decode


class ImageReader():
    """_summary_
    """
    def __init__(self, file):
        self.file = file
        self.file_name = str(file)
        self.file_extension = self.file_name.split('.')[-1]
        self.image_url = os.path.join(os.getcwd(), self.file_name)
        self.img = cv2.imread(self.image_url)

    def read_image(self):
        codes = []
        for code in decode(self.img):
            # print(code.type)
            codes.append(code.data.decode('utf-8'))
        return codes
    

    def handle_uploaded_file(self):
        """This function is a helper for reading the uploaded file
        and extract info from it
        """
        print(self.file)
        print(self.img)
        with open(f'test.{self.file_extension}', 'wb+') as destination:
            for chunk in self.file.chunks():
                print(chunk)
                destination.write(chunk)

        
class Stringb64Reader():
    def __init__(self, img_data_string):
        self.img_data_str = str(img_data_string)
        self.image_url = None
        self.img = None
    
    def string_to_PNG(self):
        self.img_data_str = self.img_data_str.split(',')[1]
        missing_padding = len(self.img_data_str) % 4
        if missing_padding:
                self.img_data_str += '=' * (4 - missing_padding)
        imgdata = base64.b64decode(self.img_data_str)
        with open('test_webcam.png', 'wb+') as destination:
            destination.write(imgdata)
        self.image_url = os.path.join(os.getcwd(), 'test_webcam.png')
        self.img = cv2.imread(self.image_url)

    def read_image(self):
        codes = []
        for code in decode(self.img):
            # print(code.type)
            codes.append(code.data.decode('utf-8'))
        return codes
