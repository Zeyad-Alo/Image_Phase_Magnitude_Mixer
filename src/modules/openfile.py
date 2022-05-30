# OLD CODE... REMOVE THIS COMMENT WHEN DONE MODIFYING

from PyQt5.QtWidgets import QFileDialog
import matplotlib.pyplot as plt
import numpy as np
from modules import interface
from PIL import Image as PILImage

# from modules.utility import print_debug

from modules.mixer import *


def browse_window(self, image_idx=1):
    self.filename = QFileDialog.getOpenFileName(
        None, 'open the signal file', './', filter="Raw Data(*.bmp *.jpg *.png)")
    path = self.filename[0]
    print_debug("Selected path: " + path)

    if path == '':
        raise Warning("No file selected")
        return

    data = open_file(self, path)

    if (image_idx == 1):
        self.image1_configured = ImageConfiguration(
            Image(path=path, data=data, fourier_enable=True))

        # initialize feature selection
        feature_idx = self.image1_component_comboBox.currentIndex()
        self.image1_configured.set_selected_feature(index=feature_idx)

        # TODO for testing purposes abstract later in interface, update display
        interface.display_pixmap(self, 'image1',
                                 self.image1_configured.get_original_image())
        interface.display_pixmap(self, 'image1_component',
                                 self.image1_configured.get_processed_image())

    elif (image_idx == 2):

        self.image2_configured = ImageConfiguration(
            Image(path=path, data=data, fourier_enable=True))

        # initialize feature selection
        feature_idx = self.image2_component_comboBox.currentIndex()
        self.image2_configured.set_selected_feature(index=feature_idx)

        # TODO for testing purposes abstract later in interface, update display
        interface.display_pixmap(self, 'image2',
                                 self.image2_configured.get_original_image())
        interface.display_pixmap(self, 'image2_component',
                                 self.image2_configured.get_processed_image())


def open_file(self, path):

    im = PILImage.open(path)

    data = np.array(im)
    return data
