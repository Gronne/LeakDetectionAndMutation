from astropy.convolution import Gaussian2DKernel
from scipy.signal import convolve as scipy_convolve
from astropy.convolution import convolve
from scipy.ndimage.filters import gaussian_filter
from scipy import signal
import numpy as np

from Modeling import Modeling3D


class LegoDetecter:
    def __init__(self, file_picture_manager):
        self.FP = file_picture_manager


    def detect_lego_pictures(self, picture_addresses):
        lego_picture_addresses = []

        for picture_address in picture_addresses:
            try:
                img = self.FP.load_picture(picture_address)

                if self.is_lego(img) == True:
                    lego_picture_addresses.append(picture_address)
                    print("Lego")
            except:
                print("Not able to Analyse image: " + picture_address)

        return lego_picture_addresses


    def is_lego(self, picture):
        for col in picture:
            for element in col:
                if element[0] != element[1] or element[0] != element[2]:
                    return False
        return True





class LeakDetecter:
    def __init__(self, file_picture_manager, models_adaptions):
        self.FP = file_picture_manager
        self.models_adaptions = models_adaptions


    def detect_leak_pictures(self, picture_addresses, threadhole_value):
        leak_picture_addresses = []
        leak_snapshot_addresses = []

        for picture_address in picture_addresses:
            try:
                img = self.FP.load_picture(picture_address)

                [status, snapshot_address] = self.is_leak(img, threadhole_value)
                if status == True:
                    leak_picture_addresses.append(picture_address)
                    leak_snapshot_addresses.append(snapshot_address)
                    print("Leak")
            except:
                print("Not able to Analyse image: " + picture_address)

        return [leak_picture_addresses, leak_snapshot_addresses]


    def is_leak(self, picture, threadhole_value):
        image_blurred = gaussian_filter(picture, sigma=(len(picture)/10))
        snapshot_addresses = self.models_adaptions.get_snapshot_addresses()

        for snapshot_address in snapshot_addresses:
            leak_picture = self.FP.load_picture(snapshot_address)
            leak_blurred = gaussian_filter(leak_picture, sigma=(len(leak_picture)/10))

            corr_coef_value = np.corrcoef(image_blurred.flat, leak_blurred.flat)[0,1]
            print("corr_coef_value: " + str(corr_coef_value))

            if corr_coef_value >= threadhole_value:
                return [True, snapshot_address]
        return [False, None]











#Nothing
