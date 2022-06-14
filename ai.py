#keras.layers import Input, Lambda, Dense, Flatten,Dropout,Conv2D,MaxPooling2D, BatchNormalization
#from keras.optimizers import SGD
from telnetlib import SE
from keras.models import load_model
#from keras.preprocessing import image
#from sklearn.metrics import accuracy_score,classification_report,confusion_matrix
#from keras.preprocessing.image import ImageDataGenerator
#from sklearn.model_selection import train_test_split
#from keras.models import Sequential
from os import makedirs 
import pandas as pd
import numpy as np
from PIL import Image
from report import generate_report, Reporter
from filemanager import FileManager
from sequence import DCMSequence
from preprocessor import Preprocessor
from settings import Settings
import matplotlib.pyplot as plt
import sys 
import argparse


class PulmonaryEmbolismDetector():
    def __init__(self):

        self.model = load_model("models/classifier/best_resnet50.h5")
        #self.model = load_model("models/classifier/resnet50.h5")
        #self.model.load_weights("models/classifier/resnet50_weights.h5")

        #self.model = load_model("models/classifier/best_googlenet.h5")
        #self.model = load_model("models/classifier/googlenet.h5")
        #self.model.load_weights("models/classifier/googlenet_weights.h5")

        #self.model = load_model("models/classifier/best_cnn.h5")
        #self.model = load_model("models/classifier/cnn.h5")
        #self.model.load_weights("models/classifier/cnn_weights.h5")

        #self.model = load_model("models/classifier/best_squeezenet.h5")
        #self.model = load_model("models/classifier/squeezenet.h5")
        #self.model.load_weights("models/classifier/squeezenet_weights.h5")
        #===================================================================#
        self.location_model = load_model('models/localizer/best_model.h5')
        #self.location_model.load_weights("models/localizer/weights.h5")

        self.preprocessor = Preprocessor()

        self.reporter = Reporter()

        self. progressBar = None

        self.config = {}

    

    def save(self, initdir, filename, img, outputdir):

        #this function is to remove the ".dcm" at the end of the filename so that when saving its not saved as "file.dcm.jpg"
        #or if the filename doesnt have any extension just return it cuz some dcm images dont have any extension
        def stripper(path:str):
            x = path.split('.')
            #if there is only 1 element in list that means there are no .dcm extension to consider
            if len(x) == 1:
                return path
            elif path[-3:] == 'dcm':
                return path[:-4]
            elif path[-3:] == 'jpg':
                return path[:-4]
            elif path[-4:] == 'jpeg':
                return path[:-5]
            elif path[-3:] == 'png':
                return path[:-4]

        #before the jpg file is saved the new directories need to be made incase it doesnt exist
        #this returns path without the filename 
        def justfolders(path:str):
            folders = path.split('/')
            path_way = ''
            for x in range(len(folders)-1):
                if folders[x] != '':
                    path_way += '/' + folders[x]
            return path_way

        image = img.reshape(512, 512)
        image = Image.fromarray(image)

        if outputdir[-1] != '/':
            outputdir += '/'

        if self.config['structure'] == 'copy':

            makedirs(outputdir+justfolders(filename), exist_ok=True)
            image.save('{}.{}'.format(outputdir+stripper(filename), self.config['format']))
       
        elif self.config['structure'] == 'one':

            makedirs(outputdir, exist_ok=True)
            image.save('{}.{}'.format(outputdir+ stripper(filename.split('/')[-1]), self.config['format']))


    def detect(self, inputdir, outputdir:str, progress=None, progressDes=None):

        self.config = Settings.config

        self.reporter.config = self.config

        self.progressBar = progress

        threshold = self.config['probability'] / 100

        def thresholder(x):
            if x >= threshold:
                return 1
            else:
                return 0

        #set lung localizer on or off
        if self.config['localizer'] == True:
            self.preprocessor.set_mode(True)
        else:
            self.preprocessor.set_mode(False)

        
        #=========================================================================#

        total = len(inputdir)

        for index, dir in enumerate(inputdir): 
            print(dir)

            if progressDes != None:
                progressDes.setText("{}/{}".format(index+1,total))

            fm = FileManager()
            files = fm.tree(dir)
            sq = DCMSequence(files)
            files = sq.get_sq()

            #preprocessor sorts the squence of files, localize lungs and transform img
            self.preprocessor.ssf(files)

            datalength = self.preprocessor.datasum()

            for i in range(datalength):
                img, name, root = self.preprocessor.iterator()
                img = img.reshape(1,512,512,3)
                

                #present = self.model(img, training=False).numpy()[0]
                present = self.model.predict(img, verbose=0)[0][0]

                location = [0,0,0]
                if present >= threshold:
                    location = self.location_model.predict(img, verbose=0)[0]

                #print("{} {}".format(present, location))

                present = thresholder(present)
                location[0] = thresholder(location[0])
                location[1] = thresholder(location[1])
                location[2] = thresholder(location[2])
                data = {'root':root, 'image': name, 'pe_present_on_image': present, 'leftsided_pe': location[0],'central_pe': location[1],'rightsided_pe': location[2]}
                #data = {'root':root, 'image': name, 'pe_present_on_image': f"{present:04}", 'leftsided_pe': f"{location[0]:04}",'central_pe': f"{location[1]:04}",'rightsided_pe': f"{location[2]:04}" }
                #data = {'image': name, 'pe_present_on_image': f"{present:04}", 'leftsided_pe': 0,'central_pe': 1,'rightsided_pe': 2 }


                #self.results = pd.concat([self.results, pd.DataFrame([data])], ignore_index=True)
                self.reporter.sop_lvl_adder(data)


                if self.progressBar != None:
                    self.progressBar.setValue(int(((i+1) / datalength) * 100))

                

            self.reporter.sop_concluder()
            self.reporter.generate_sop_report(outputdir=outputdir)
            self.reporter.reset_sop()

        
        self.reporter.generate_study_report(outputdir=outputdir)
        self.reporter.reset_study()

        if self.progressBar != None:
            progressDes.setText("")
            self.progressBar.setValue(0)

        
    



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, metavar='path/to/inputfiles')
    parser.add_argument('--output', required=True, metavar='path/to/outputfiles')
    args = parser.parse_args()
    outputdir = args.output
    inputdir = args.input.split(',')
    from filemanager import FileManager
    from sequence import DCMSequence
    from preprocessor import Preprocessor
    ai = PulmonaryEmbolismDetector()
    ai.detect(inputdir=inputdir, outputdir=outputdir)



    
