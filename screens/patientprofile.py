from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QFileDialog
from database import DBManager
from models import Patient


class PatientProfileScreen(QDialog):

    def __init__(self, app_map, widget):
        super(PatientProfileScreen, self).__init__()
        from os import getcwd
        loadUi(getcwd()+"/screens/ui/patientprofile.ui", self)
        self.app_map = app_map
        self.widget = widget

        self.pushButton.clicked.connect(self.edit)
        self.pushButton_5.clicked.connect(self.cancel)
        self.pushButton_4.clicked.connect(self.delete)


    def edit(self):
        #acess that screen with data alreaady loaded and linked for that id

        self.widget.setCurrentIndex(self.app_map['patient'])

    def cancel(self):
        self.widget.setCurrentIndex(self.app_map['home'])

    def delete(self):
        id = 1#get the data here
        DBManager.del_row(obj=Patient, id=id)
        self.widget.setCurrentIndex(self.app_map['home'])



    

#check current widget index
#widget.currentIndex()
