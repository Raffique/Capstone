import os

cwd = os.path.abspath(os.getcwd())

cmm1 = "pip install -r requirements.txt"
cmm2 = 'pyinstaller --onefile --add-data="{}/login.ui:." --add-data="{}/main.ui:." --add-data="{}/model2.h5:." --add-data="{}/report.html:." -F --collect-submodules=pydicom gui.py'.format(cwd, cwd, cwd, cwd)

os.system(cmm1)
os.system(cmm2)