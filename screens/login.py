from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QStackedWidget, QFileDialog



class LoginScreen(QDialog):
    def __init__(self, app_map, widget):
        super(LoginScreen, self).__init__()
        from os import getcwd
        loadUi(getcwd()+"/screens/ui/login.ui", self)
        self.app_map = app_map
        self.widget = widget

        self.pushButton.clicked.connect(self.login)
        self.pushButton_2.clicked.connect(self.register)
        self.pushButton_3.clicked.connect(self.gotohome)
        self.pushButton_4.clicked.connect(self.recover)
        

    def login(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        if username == "" or password == "":
            pass
            #make a popup show
            return
        #check if password match wha is in data
        #then move onto main

    def register(self):
        pass
        #self.widget.setCurrentIndex(self.app_map['register'])

    def gotohome(self):
        self.widget.setCurrentIndex(self.app_map['home'])

    def recover(self):
        pass
        #self.widget.setCurrentIndex(self.app_map['recover'])