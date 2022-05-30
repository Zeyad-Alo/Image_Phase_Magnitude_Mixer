# define class and related functions
from copy import copy, deepcopy
from dataclasses import dataclass, field
from typing import ClassVar
from scipy.fft import fftfreq, fft, ifft, fft2, ifft2, fftn, ifftn
import numpy as np
from sympy import fourier_transform
from modules.utility import *
import PyQt5.QtCore
from PyQt5.QtWidgets import QMessageBox

# frozen = True means that the class cannot be modified
# kw_only = True means that the class cannot be instantiated with positional arguments


@dataclass
class ImageFFT():

    image_data: np.array

    fftfreq: np.ndarray = None
    fftphase: np.ndarray = None
    fftmag: np.ndarray = None
    uniform_phase: np.ndarray = None
    uniform_magnitude: np.ndarray = None
    fftreal: np.ndarray = None
    fftimag: np.ndarray = None

    fftdata: np.array = None

    def __post_init__(self):
        self.process_image()

    def process_image(self):
        # TODO: 2D fft??
        self.fftdata = fftn(self.image_data)

        # TODO: is this correct?
        # self.fftfreq = fftfreq(self.data.size, 1 / 44100)
        self.fftreal = np.real(self.fftdata)
        self.fftimag = np.imag(self.fftdata)
        self.fftmag = np.abs(self.fftdata)
        self.fftphase = np.angle(self.fftdata)

        # TODO: check if this is correct
        self.uniform_phase = np.multiply(self.fftmag, np.exp(1j))
        self.uniform_magnitude = np.multiply(1, np.exp(self.fftphase))


@dataclass()
class Image():

    data: np.ndarray  # required on init
    path: str = ''
    image_height: int = 0
    image_width: int = 0
    image_depth: int = 0
    fourier_enable: bool = False
    image_fft: ImageFFT = None

    def __post_init__(self):
        self.update_parameters()
        if (self.fourier_enable):
            self.init_fourier()

    def init_fourier(self):
        self.image_fft = ImageFFT(image_data=self.data)

    def update_parameters(self):
        # TODO: calculate basic parameters (width, height, etc)
        self.image_height = self.data.shape[0]
        self.image_width = self.data.shape[1]
        self.image_depth = self.data.shape[2]


# contains all the fourier transformed data of an image
# on performs fft2 on initialization
@dataclass
class ImageConfiguration():
    image: Image
    selected_feature: str = "Full"
    selected_feature_index: int = 6
    strength_percent: int = 100

    selected_feature_dict: ClassVar[dict] = {
        "Phase": 0,
        "Magnitude": 1,
        "Uniform_Phase": 2,
        "Uniform_Magnitude": 3,
        "Real": 4,
        "Imaginary": 5,
        "Full": 6
    }
    ''' Global to all class instances'''

    def set_weight(self, weight):
        self.strength_percent = weight

    def set_selected_feature(self, feature=None, index=None):
        '''Sets the selected feature based on its index or name'''
        if feature is not None:
            self.selected_feature_index = self.convert_feature_to_index(
                feature)
            self.selected_feature = feature

        elif index is not None:
            self.selected_feature = self.convert_index_to_feature(index)
            self.selected_feature_index = index
        else:
            raise Exception("Invalid Inputs")

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

    def get_original_image(self):
        return self.image.data

    def get_processed_image(self):
        '''Selects image based on required feature then \n
        internaly weighs images based on the strength_percent'''

        if(self.selected_feature == "Phase"):
            image = copy(self.image.image_fft.fftphase)
        elif(self.selected_feature == "Magnitude"):
            image = copy(self.image.image_fft.fftmag)
        elif(self.selected_feature == "Uniform_Phase"):
            image = copy(self.image.image_fft.uniform_phase)
        elif(self.selected_feature == "Uniform_Magnitude"):
            image = copy(self.image.image_fft.uniform_magnitude)
        elif(self.selected_feature == "Real"):
            image = copy(self.image.image_fft.fftreal)
        elif(self.selected_feature == "Imaginary"):
            image = copy(self.image.image_fft.fftimag)
        elif(self.selected_feature == "Full"):
            image = copy(self.image.image_fft.fftdata)
        else:
            raise Exception("Invalid Feature")

        # modify magnitude component and restore phase
        # weighted_image_fft = np.multiply(np.multiply(np.abs(
        #     image), self.strength_percent / 100), np.exp(np.multiply(np.angle(image), 1j)))

        # TODO: convert from FFT coefficients to image after applying weights
        weighted_image = ifftn(
            image * self.strength_percent/100).astype(np.uint8)

        return weighted_image


class ImageMixer():
    def __init__(self, image_1: Image, image_2: Image) -> None:
        self.input_images = [image_1, image_2]
        self.selected_images = [ImageConfiguration(
            image_1), ImageConfiguration(image_2)]
        self.preview_images = [Image(), Image()]
        self.output_images = [Image(), Image()]
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
        '''Mix images based on selected features in the frequency domain'''

        # if all is good then mix

        # additive weighted mixing
        self.mixed_image.set_data(
            self.selected_images[0].get_processed_image()
            + self.selected_images[1].get_processed_image())
