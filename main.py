import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget
from screens.login import LoginScreen
from screens.home import HomeScreen
from screens.patient import PatientScreen
from screens.patientprofile import PatientProfileScreen
from screens.scan import ScanScreen
from screens.scanprofile import ScanProfileScreen
from screens.config import ConfigScreen
#from settings import SettingsScreen

#The map should match the order the respective widgets are added


if __name__ == "__main__":

    app = QApplication(sys.argv)
    widget = QStackedWidget()
     
    widget.setFixedHeight(600)
    widget.setFixedWidth(800)

    #make sure the mapping match the amount of widgets in stack
    app_map = {'login': 0, 'home': 1, 'patient': 2, 'patientprofile': 3, 'scan':4, 'scanprofile':5, 'settings': 6}
    
    #Place all screens here
    widget.addWidget(LoginScreen(app_map, widget))
    widget.addWidget(HomeScreen(app_map, widget))
    widget.addWidget(PatientScreen(app_map, widget))
    widget.addWidget(PatientProfileScreen(app_map, widget))
    widget.addWidget(ScanScreen(app_map, widget))
    widget.addWidget(ScanProfileScreen(app_map, widget))
    widget.addWidget(ConfigScreen(app_map, widget))


    widget.show()
    try:
        sys.exit(app.exec_())
    except:
        print("Exiting")