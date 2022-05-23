from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QFileDialog
from database import DBManager
from models import Patient


class PatientScreen(QDialog):

    def __init__(self, app_map, widget):
        super(PatientScreen, self).__init__()
        from os import getcwd
        loadUi(getcwd()+"/screens/ui/patient.ui", self)
        self.app_map = app_map
        self.widget = widget

        self.pushButton.clicked.connect(self.save)
        self.pushButton_5.clicked.connect(self.cancel)
        self.pushButton_4.clicked.connect(self.config)


    def save(self):
        hid = self.lineEdit.text()
        name = self.lineEdit_2.text()
        notes = self.lineEdit_5.text()
        age = self.spinBox.value()
        gender = ''
        if self.radioButton.is_Checked():
            gender = 'm'
        else:
            gender = 'f'
        dob = self.dateEdit.text()
        p = Patient(hid=hid, name=name, notes=notes, age=age, gender=gender, dob=dob)
        DBManager.add_row(p)

        self.widget.setCurrentIndex(self.app_map['patientprofile'])

    def cancel(self):
        self.widget.setCurrentIndex(self.app_map['home'])

    def config(self):
        self.widget.setCurrentIndex(self.app_map['setings'])



    

#check current widget index
#widget.currentIndex()
