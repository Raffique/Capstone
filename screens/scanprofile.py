from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QFileDialog
from database import DBManager
from models import Scan


class ScanProfileScreen(QDialog):

    def __init__(self, app_map, widget):
        super(ScanProfileScreen, self).__init__()
        from os import getcwd
        loadUi(getcwd()+"/screens/ui/scanprofile.ui", self)
        self.app_map = app_map
        self.widget = widget

        self.pushButton.clicked.connect(self.cancel)
        self.pushButton_2.clicked.connect(self.generate)
        self.pushButton_3.clicked.connect(self.view)
        self.pushButton_4.clicked.connect(self.delete)

    def generate(self):
        pass

    def view(self):
        pass

    def cancel(self):
        self.widget.setCurrentIndex(self.app_map['home'])

    def delete(self):
        id = 1#get the data here
        DBManager.del_row(obj=Scan, id=id)
        self.widget.setCurrentIndex(self.app_map['home'])



    

#check current widget index
#widget.currentIndex()
