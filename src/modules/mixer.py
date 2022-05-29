# define class and related functions

from dataclasses import dataclass
from scipy.fft import rfftfreq, rfft, irfft
import numpy as np
from modules.utility import *
import PyQt5.QtCore
from PyQt5.QtWidgets import QMessageBox


@dataclass
class Image():

    path: str
    data: np.ndarray = None
    image_height = 0
    image_width = 0
    fftdata: np.ndarray = None
    fftfreq: np.ndarray = None
    uniform_phase: np.ndarray = None
    uniform_magnitude: np.ndarray = None
    phase: np.ndarray = None
    magnitude: np.ndarray = None

    def set_data(self, data):
        self.data = data
        # TODO: check if it makes sense to process the image here
        # process_image(self)

    def update_parameters(self):
        # TODO: calculate basic parameters (width, height, etc)
        pass

    def process_image(self):
        self.fftdata = rfft(self.data)

        # TODO: is this correct?
        self.fftfreq = rfftfreq(self.data.size, 1 / 44100)
        self.fftreal = np.real(self.fftdata)
        self.fftimag = np.imag(self.fftdata)
        self.fftmag = np.abs(self.fftdata)
        self.fftphase = np.angle(self.fftdata)

        # TODO: check if this is correct
        self.uniform_phase = np.multiply(self.fftmag, np.exp(1j))
        self.uniform_magnitude = np.multiply(1, np.exp(self.fftphase))

    def get_real(self):
        return self.fftreal

    def get_imag(self):
        return self.fftimag

    def get_fft(self):
        return self.fftdata

    def get_fftfreq(self):
        return self.fftfreq

    def get_uniform_phase(self):
        return self.uniform_phase

    def get_uniform_magnitude(self):
        return self.uniform_magnitude

    def get_data(self):
        return self.data


@dataclass
class ImageConfiguration():
    image: Image
    selected_feature: str
    selected_feature_index: int
    strength_percent: int = 100
    selected_feature_dict: dict = {
        "Phase": 0,
        "Magnitude": 1,
        "Uniform_Phase": 2,
        "Uniform_Magnitude": 3,
        "Real": 4,
        "Imaginary": 5
    }

    def set_weight(self, weight):
        self.strength_percent = weight

    def set_feature(self, feature):
        if feature in self.selected_feature_dict:
            self.selected_feature = feature
            self.selected_feature_index = self.selected_feature_dict[feature]
        else:
            raise Exception("Invalid Feature")

    def convert_feature_to_index(self, feature):
        if feature in self.selected_feature_dict:
            return self.selected_feature_dict[feature]
        else:
            raise Exception("Invalid Feature")

    def convert_index_to_feature(self, index):
        for key, value in self.selected_feature_dict.items():
            if value == index:
                return key
        raise Exception("Invalid Index")

    def get_processed_image(self):
        '''Selects image based on required feature then \n
        internaly weighs images based on the strength_percent'''

        if(self.selected_feature == "Phase"):
            image = self.image.get_phase()
        elif(self.selected_feature == "Magnitude"):
            image = self.image.get_magnitude()
        elif(self.selected_feature == "Uniform_Phase"):
            image = self.image.get_uniform_phase()
        elif(self.selected_feature == "Uniform_Magnitude"):
            image = self.image.get_uniform_magnitude()
        elif(self.selected_feature == "Real"):
            image = self.image.get_real()
        elif(self.selected_feature == "Imaginary"):
            image = self.image.get_imag()
        else:
            raise Exception("Invalid Feature")

        # TODO: convert from FFT coefficients to image if not already done

        weighted_image = image.data * self.strength_percent / 100

        return weighted_image


class ImageMixer():
    def __init__(self, image_1=Image(), image_2=Image()) -> None:
        self.input_images = [image_1, image_2]
        self.selected_images = [ImageConfiguration(), ImageConfiguration()]
        self.mixed_image = Image()

    def reset_selection(self):
        '''Reset image selections'''
        self.input_images[0].reset_selection()

    # TODO: dont forget image size check
    def set_input_image(self, image: Image, image_idx):
        self.input_images[image_idx] = image
        self.selected_images[image_idx].image = image

    def set_selected_feature(self, idx, feature):
        self.selected_images[idx].set_feature(feature)

    def set_selected_image(self, idx, feature):
        pass

    def mix_images(self):
        '''Mix images based on selected features'''

        # if all is good then mix

        # additive weighted mixing
        self.mixed_image.set_data(
            self.selected_images[0].get_processed_image()
            + self.selected_images[1].get_processed_image())


def update_display(self, display_idx: int):
    pass
