import os
import base64
import cv2

import tempfile

from PIL import Image

from pyzbar.pyzbar import decode


class ImageReader:
    """Helper class scanning images from file upload for barcode
    Handles image reading when a whole image file is uploaded
    -- read the file, save it in a tempfile and find barcode
    """

    def __init__(self, file):
        self.file = file
        self.file_extension = "." + str(self.file).split(".")[-1]

    def get_image_barcode(self):
        codes = []
        img = Image.open(self.file.file)

        with tempfile.NamedTemporaryFile(suffix=self.file_extension) as destination:
            img.save(destination)
            file_url = os.path.join(tempfile.gettempdir(), destination.name)
            read_image = cv2.imread(file_url)
            for code in decode(read_image):
                codes.append(code.data.decode("utf-8"))
        return codes


class Stringb64Reader:
    """Helper class scanning images from webcam upload for barcode
    Handles image reading when a webcam capture image b64 string is uploaded
    -- read the string, bring it back to image data, save it in a tempfile
    and find barcode
    """

    def __init__(self, img_data_string):
        self.img_data_str = str(img_data_string)
        self.img = None

    def string_to_PNG(self):
        self.img_data_str = self.img_data_str.split(",")[1]
        missing_padding = len(self.img_data_str) % 4
        if missing_padding:
            self.img_data_str += "=" * (4 - missing_padding)
        imgdata = base64.b64decode(self.img_data_str)
        with tempfile.NamedTemporaryFile(suffix=".png") as destination:
            destination.write(imgdata)
            file_url = os.path.join(tempfile.gettempdir(), destination.name)
            self.img = cv2.imread(file_url)

    def read_image(self):
        codes = []
        for code in decode(self.img):
            codes.append(code.data.decode("utf-8"))
        return codes
