
from PyQt5.QtWidgets import QTabWidget, QAction, QPushButton, QSlider, QComboBox, QLCDNumber, QMessageBox
from PyQt5.QtGui import *
import openfile
# interface globals
CreatorSelectedIndex = 0
''' Sould be connected to the combobox on change'''
ToggleSecondary = True
''' If true then visible'''


def init_connectors(self):
    '''Initializes all event connectors and triggers'''

    ''' Menu Bar'''
    self.actionOpen = self.findChild(QAction, "actionOpen")
    self.actionOpen.triggered.connect(
        lambda: openfile.browse_window(self))

    self.actionExport = self.findChild(QAction, "actionExport")
    self.actionExport.triggered.connect(
        lambda: openfile.export_summed_signal(self))

    self.actionAbout_Us = self.findChild(QAction, "actionAbout_Us")
    self.actionAbout_Us.triggered.connect(
        lambda: about_us(self))

    self.WindowTabs = self.findChild(QTabWidget, "WindowTabs")


def about_us(self):
    QMessageBox.about(
        self, ' About ', 'This is a nyquist theory illustrator \nCreated by junior students from the faculty of Engineering, Cairo Uniersity, Systems and Biomedical Engineering department \n \nTeam members: \n-Mohammed Nasser \n-Abdullah Saeed \n-Zeyad Mansour \n-Mariam Khaled \n \nhttps://github.com/mo-gaafar/Nyquist_Theory_Illustrator.git ')
