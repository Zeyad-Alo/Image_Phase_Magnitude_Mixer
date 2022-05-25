# define class and related functions

from dataclasses import dataclass
from scipy.fft import rfftfreq, rfft, irfft
import numpy as np
from modules.utility import *
from modules import spectrogram as spectro
import PyQt5.QtCore
import pyqtgraph as pg
import pygame
from PyQt5.QtWidgets import QMessageBox


class ImageMixer():
    def __init__(self, image_1, image_2) -> None:
        pass


@dataclass
class Image():
    path: str
    data: np.ndarray
    fftdata = rfft(data)
    fftfreq = rfftfreq(data.size, 1 / 44100)
    fftreal = np.real(fftdata)
    fftimag = np.imag(fftdata)
    fftmag = np.abs(fftdata)
    fftphase = np.angle(fftdata)

    def get_real(self):
        return self.data.real

    def get_imag(self):
        return self.data.imag

    def get_fft(self):
        return self.fftdata

    def get_fftfreq(self):
        # return rfftfreq(self.data.size, 1 / 44100)
        pass

    def get_data(self):
        return self.data


def update_image(self):
    pass
