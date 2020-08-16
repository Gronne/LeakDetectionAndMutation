import numpy as np
from PIL import Image


class FilePictureManagement:
    def __init__(self):
        pass

    def move_pictures(self, picture_urls, saving_url):
        for picture_url in picture_urls:
            img = self.load_picture(picture_url)
            self.save_picture(img, saving_url, picture_url.split('/')[-1])


    def save_picture(self, img, address, name):
        im = Image.fromarray(img)
        im.save(address + name)


    def load_picture(self, address):
        img = Image.open(address) #problem
        return np.array(img)








#Nothing
