from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QFileDialog
import settings
import models
from database import DBManager


class ConfigScreen(QDialog):

    def __init__(self, app_map, widget):
        super(ConfigScreen, self).__init__()
        from os import getcwd
        loadUi(getcwd()+"/screens/ui/config.ui", self)
        self.app_map = app_map
        self.widget = widget

        self.pushButton.clicked.connect(self.save) #save
        self.pushButton_5.clicked.connect(self.cancel) #cancel

        self.config = settings.Settings.config
        self.checkBox_3.setChecked(self.config['localizer'])
        self.checkBox.setChecked(self.config['pdf'])
        self.checkBox_2.setChecked(self.config['csv'])
        if self.config['pic_format'] == 'jpg':
            self.radioButton_3.setChecked(True)
        elif self.config['pic_format'] == 'png':
            self.radioButton_4.setChecked(True)
        if self.config['results'] == 'binary':
            self.radioButton_5.setChecked(True)
        elif self.config['results'] == 'dots':
            self.radioButton_6.setChecked(True)
        elif self.config['results'] == 'sticky':
            self.radioButton_7.setChecked(True)
        elif self.config['results'] == 'word':
            self.radioButton_8.setChecked(True)
        self.spinBox.setValue(self.config['probability'])
        

    def save(self):
        localizer = self.checkBox_3.isChecked()
        pdf = self.checkBox.isChecked()
        csv = self.checkBox_2.isChecked()
        pic= ''
        if self.radioButton_3.isChecked():
            pic = 'jpg'
        else:
            pic = 'png'
        v3d = self.checkBox_4.isChecked()

        results = ''
        if self.radioButton_5.isChecked():
            results = 'binary'
        elif self.radioButton_6.isChecked():
            results = 'dots'
        elif self.radioButton_7.isChecked():
            results = 'sticky'
        elif self.radioButton_8.isChecked():
            results = 'words'

        probability = self.spinBox.value()

        settings.Settings.mod(localizer=localizer, pdf=pdf, csv=csv, pic_format=pic, v3d=v3d, results=results, probability=probability)

        self.widget.setCurrentIndex(self.app_map['home'])

    def cancel(self):
        self.widget.setCurrentIndex(self.app_map['home'])




    

#check current widget index
#widget.currentIndex()
