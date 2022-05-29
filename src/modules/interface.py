
from turtle import onrelease
from PyQt5.QtWidgets import QTabWidget, QAction, QPushButton, QSlider, QComboBox, QLCDNumber, QMessageBox
from PyQt5.QtGui import *
from modules import openfile

def init_connectors(self):
    '''Initializes all event connectors and triggers'''

    # ''' Menu Bar'''
    # self.actionOpen = self.findChild(QAction, "actionOpen")
    # self.actionOpen.triggered.connect(
    #     lambda: openfile.browse_window(self))

    # self.actionExport = self.findChild(QAction, "actionExport")
    # self.actionExport.triggered.connect(
    #     lambda: openfile.export_summed_signal(self))

    # self.actionAbout_Us = self.findChild(QAction, "actionAbout_Us")
    # self.actionAbout_Us.triggered.connect(
    #     lambda: about_us(self))

    # self.WindowTabs = self.findChild(QTabWidget, "WindowTabs")

    ''' Browse buttons'''
    # TODO dont forget to add new argument to browse_window

    # the index argument maps each function to its respective slot
    #
    self.insert_image1_pushButton.clicked.connect(
        lambda: openfile.browse_window(self, 1))
    self.insert_image2_pushButton.clicked.connect(
        lambda: openfile.browse_window(self, 2))

    ''' Image Component Dropdowns'''
    # 1. on index change
    # 2. change component in image configuration
    # 3. display image configuration component using pixmap?

    ''' Image Mixer'''
    # uses image configurations already made
    # selects index of images to be mixed
    # TODO how to deal with image 1, image 1 for example, in the most efficient way?

    # TODO Add output selection functionality somewhere
    #outside class function then refresh selected display
    self.mixer_output_comboBox.currentIndexChanged.connect(
        # lambda: ?? 
    )

    #inside class function then refresh display (from class info)
    self.mixer_component1_comboBox.currentIndexChanged.connect(
        # lambda: #change configuration's component from default to new index
    )
    self.mixer_component2_comboBox.currentIndexChanged.connect(
        # change ?????????
    )
    self.mixer_component1_horizontalSlider.released.connect(
        # lambda: #change configuration's strength
    )
    self.mixer_component2_horizontalSlider.released.connect(
        # change configuration's strength
    )



def about_us(self):
    QMessageBox.about(
        self, ' About ', 'This is a nyquist theory illustrator \nCreated by junior students from the faculty of Engineering, Cairo Uniersity, Systems and Biomedical Engineering department \n \nTeam members: \n-Mohammed Nasser \n-Abdullah Saeed \n-Zeyad Mansour \n-Mariam Khaled \n \nhttps://github.com/mo-gaafar/Nyquist_Theory_Illustrator.git ')
