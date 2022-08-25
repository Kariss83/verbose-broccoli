import os

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

        Args:
            extension (str): the extension that's on the end of the file's
                            name

        Returns:
            list: a list of codes you can find in the uploaded picture
        """
        with open(f'test.{self.file_extension}', 'wb+') as destination:
            for chunk in self.file.chunks():
                destination.write(chunk)
        

