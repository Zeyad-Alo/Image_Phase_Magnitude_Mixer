# OLD CODE... REMOVE THIS COMMENT WHEN DONE MODIFYING

from PyQt5.QtWidgets import QFileDialog
import matplotlib.pyplot as plt
import numpy as np

from PIL import Image

from modules.utility import print_debug

from modules.mixer import *


def browse_window(self):
    self.graph_empty = False
    self.filename = QFileDialog.getOpenFileName(
        None, 'open the signal file', './', filter="Raw Data(*.bmp *.jpg *.png)")
    path = self.filename[0]
    print_debug("Selected path: " + path)
    open_file(self, path)
    # play the sound


def open_file(self, path):

    im = Image.open(path)

    data = np.array(im)

    self.image_data = Image(path, data)
    self.pointsToAppend = 0
