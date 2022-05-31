from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QFileDialog
#from cycles import Cycler
from ai import PulmonaryEmbolismDetector
from filemanager import FileManager
from sequence import DCMSequence
from settings import Settings
from os import listdir

class ScanScreen(QDialog):

    def __init__(self, app_map, widget):
        super(ScanScreen, self).__init__()
        from os import getcwd
        loadUi(getcwd()+"/screens/ui/scan.ui", self)
        self.app_map = app_map
        self.widget = widget
        self.detector = PulmonaryEmbolismDetector()

        self.outputdir = ''
        self.inputdir = ''
        
        self.file_or_folder = 'folder'

        self.pushButton_9.clicked.connect(self.add)
        self.pushButton_10.clicked.connect(self.remove)
        self.pushButton_2.clicked.connect(self.input_directory) #input
        self.pushButton_7.clicked.connect(self.input_file) #input
        self.pushButton_3.clicked.connect(self.output_directory) #output

        self.pushButton.clicked.connect(self.start) #start scanning
        self.pushButton_5.clicked.connect(self.stop) #stop
        self.pushButton_4.clicked.connect(self.settings) # settings
        self.pushButton_6.clicked.connect(self.view)
        self.pushButton_8.clicked.connect(self.cancel)
        #self.prograssBar

    
    def add(self):
        #print(self.combo_box.count())
        #self.combo_box.itemText(i)
        #self.combo_box.currentText()
        #self.combo_box.currentIndex()
        #self.combo_box.setCurrentIndex(2)
        #self.combo_box.setCurrentText(item)
        #self.combo_box.clear() # remove all items
        #self.combo_Box.removeItem(index)
        #self.combo_Box.findText(text) # find the index


        dir = self.lineEdit.text()
        if dir != '' and listdir(dir) and dir not in [self.comboBox.itemText(i) for i in range(self.comboBox.count())]:
            print(dir)
            self.comboBox.addItem(dir)
        else:
            pass
            print("pass")
            #pop box saying already in list or invalid
        self.lineEdit.setText('')

    def remove(self):
        pass
        index = self.comboBox.currentIndex()
        if index >= 0:
            self.comboBox.removeItem(index)
        else:
            pass
            #popup telling user  no

    def input_directory(self):
        self.inputdir = QFileDialog.getExistingDirectory(self, 'Choose a directory')
        self.lineEdit.setText(self.inputdir)

    def input_file(self):
        self.inputdir = QFileDialog.getOpenFileNames(self, 'Choose files', filter='files(*.zip)')[0]
        self.lineEdit.setText('{} files are selected'.format(len(self.inputdir)))

    def output_directory(self):
        self.outputdir = QFileDialog.getExistingDirectory(self, 'Choose a directory')
        self.lineEdit_2.setText(self.outputdir)

    def cancel(self):
        self.widget.setCurrentIndex(self.app_map['home'])


    def settings(self):
        print('settings....')


    def start(self):

        dirs = []
        if self.comboBox.count > 0:
            dirs = [self.comboBox.itemText(i) for i in range(self.comboBox.count())]

        if type(self.inputdir) != list:  
            self.inputdir = self.lineEdit.text()

        self.outputdir = self.lineEdit_2.text()
        #or saved output destination that saves report based on scan id number

        if self.outputdir[-1] != '/':
            self.outputdir += '/'
       
        if (self.inputdir != "" or type(self.inputdir) == list) and self.outputdir != "":
            print('starting....')
            fm = FileManager()
            files = fm.tree(self.inputdir)
            sq = DCMSequence(files)
            files = sq.get_sq()

            self.detector.config['lungs-localizer'] = Settings.config['localizer']
            self.detector.data(inputdir=files, outputdir=self.outputdir, progress=self.progressBar)


    def stop(self):

        pass

    def view(self):
        pass



    

#check current widget index
#widget.currentIndex()
