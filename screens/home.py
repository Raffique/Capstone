from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QFileDialog


class HomeScreen(QDialog):

    def __init__(self, app_map, widget):
        super(HomeScreen, self).__init__()
        from os import getcwd
        loadUi(getcwd()+"/screens/ui/home.ui", self)
        self.app_map = app_map
        self.widget = widget

        self.pushButton_8.clicked.connect(self.search) #search
        self.pushButton_7.clicked.connect(self.scan) #scan
        self.pushButton_6.clicked.connect(self.patient) #add patient

        self.toolButton.clicked.connect(self.config)

        self.radioButton_6.clicked.connect(self.pos) #all
        self.radioButton_5.clicked.connect(self.pos) #patient
        self.radioButton_7.clicked.connect(self.pos) #scans

        self.radioButton_4.clicked.connect(self.term)#id
        self.radioButton_3.clicked.connect(self.term)#name
        self.radioButton.clicked.connect(self.term)#date
        self.radioButton_2.clicked.connect(self.term)#positive detections

        

    def patient(self):
        self.widget.setCurrentIndex(self.app_map['patient'])

    def scan(self):
        self.widget.setCurrentIndex(self.app_map['scan'])

    def config(self):
        self.widget.setCurrentIndex(self.app_map['settings'])


    def pos(self):
        if self.radioButton_6.is_Checked():
            pass
        elif self.radioButton_5.is_Checked():
            pass
        elif self.radioButton_7.is_Checked():
            pass

    def term(self):
        if self.radioButton_4.is_Checked():
            pass
        elif self.radioButton_3.is_Checked():
            pass
        elif self.radioButton.is_Checked():
            pass
        elif self.radioButton_2.is_Checked():
            pass

    def search(self):
        pass




    

#check current widget index
#widget.currentIndex()
