# define class and related functions

from dataclasses import dataclass, field
from scipy.fft import rfftfreq, rfft, irfft
import numpy as np
from sympy import fourier_transform
from modules.utility import *
import PyQt5.QtCore
import pyqtgraph as pg
import pygame
from PyQt5.QtWidgets import QMessageBox

# frozen = True means that the class cannot be modified
# kw_only = True means that the class cannot be instantiated with positional arguments


@dataclass(frozen=True, kw_only=True)
class Image():

    path: str = ''
    data: np.ndarray = None
    image_height: int = 0
    image_width: int = 0
    image_depth: int = 0
    fourier_enable: bool = False
    image_fft: ImageFFT = field(default_factory=ImageFFT)

    def __post_init__(self):
        self.update_parameters()
        if (self.fourier_enable):
            self.process_image()

    def process_image(self):
        pass

    def update_parameters(self):
        # TODO: calculate basic parameters (width, height, etc)
        pass

# contains all the fourier transformed data of an image
# on performs fft2 on initialization


@dataclass(frozen=True, kw_only=True)
class ImageFFT():

    image: Image = field(default_factory=Image)
    fftdata: np.ndarray = field(default_factory=np.ndarray)

    fftfreq: np.ndarray = field(
        init=False, default_factory=np.ndarray, repr=False)
    uniform_phase: np.ndarray = field(
        init=False, default_factory=np.ndarray, repr=False)
    uniform_magnitude: np.ndarray = field(
        init=False, default_factory=np.ndarray, repr=False)
    phase: np.ndarray = field(
        init=False, default_factory=np.ndarray, repr=False)
    magnitude: np.ndarray = field(
        init=False, default_factory=np.ndarray, repr=False)
    real: np.ndarray = field(
        init=False, default_factory=np.ndarray, repr=False)
    imag: np.ndarray = field(
        init=False, default_factory=np.ndarray, repr=False)

    def process_image(self):
        # TODO: 2D fft??
        self.fftdata = rfft(self.data)

        # TODO: is this correct?
        # self.fftfreq = rfftfreq(self.data.size, 1 / 44100)
        self.fftreal = np.real(self.fftdata)
        self.fftimag = np.imag(self.fftdata)
        self.fftmag = np.abs(self.fftdata)
        self.fftphase = np.angle(self.fftdata)

        # TODO: check if this is correct
        self.uniform_phase = np.multiply(self.fftmag, np.exp(1j))
        self.uniform_magnitude = np.multiply(1, np.exp(self.fftphase))


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

    def set_selected_feature(self, feature):
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
        '''Mix images based on selected features in the frequency domain'''

        # if all is good then mix

        # additive weighted mixing
        self.mixed_image.set_data(
            self.selected_images[0].get_processed_image()
            + self.selected_images[1].get_processed_image())


