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

        res = ''
        if self.radioButton_5.isChecked():
            res = 'binary'
        elif self.radioButton_6.isChecked():
            res = 'dots'
        elif self.radioButton_7.isChecked():
            res = 'sticky'
        elif self.radioButton_8.isChecked():
            res = 'words'
        settings.Settings.mod(localizer=localizer, pdf=pdf, csv=csv, pic_format=pic, v3d=v3d, res=res)

        self.widget.setCurrentIndex(self.app_map['home'])

    def cancel(self):
        self.widget.setCurrentIndex(self.app_map['home'])




    

#check current widget index
#widget.currentIndex()
