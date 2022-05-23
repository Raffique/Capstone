#keras.layers import Input, Lambda, Dense, Flatten,Dropout,Conv2D,MaxPooling2D, BatchNormalization
#from keras.optimizers import SGD
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
from report import generate_report
from preprocessor import Preprocessor
import matplotlib.pyplot as plt 


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

        self. progressBar = None

        self.config = {
            'detector': True,
            'save-images' : False,
            'save-csv' : True,
            'save-report' : True,
            'structure' : 'copy',
            'format' : 'jpg',
            'lungs-localizer': False,

        }

        self.results = pd.DataFrame(columns=['image','pe_present_on_image','leftsided_pe','central_pe','rightsided_pe'])



    def data(self, inputdir:str,  outputdir:str, progress=None):

        #if file converted isnt actually a dcm image skip detecting or saving

        self.progressBar = progress

        if self.config['detector'] == True:

            self.detect(inputdir)
            self.report(outputdir)


        #change to save data to database well may
        if self.config['save-images'] == True:

            #self.save(initdir, filename, img, outputdir)
            pass
    

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


    def detect(self, inputdir):

        def binary(x):

            if x >= 1:
                return 1
            else:
                return 0

        #set lung localizer on or off
        if self.config['lungs-localizer'] == True:
            self.preprocessor.set_mode(True)
        else:
            self.preprocessor.set_mode(False)

        #preprocessor sorts the squence of files, localize lungs and transform img
        self.preprocessor.ssf(inputdir)

        datalength = self.preprocessor.datasum()

        for i in range(datalength):
            img, name = self.preprocessor.iterator()
            img = img.reshape(1,512,512,3)
            

            #present = self.model(img, training=False).numpy()[0]
            present = self.model.predict(img, verbose=0)
            print(present)
            present = [present[0]]


            if int(present[0]) >= 0.4:
                location = self.location_model(img, training=False).numpy()[0]
                location = list(map(binary, location))
            else:
                location = [0,0,0]


            data = present + location


            data = {'image': name, 'pe_present_on_image': round(data[0][0], 3), 'leftsided_pe': data[1],'central_pe': data[2],'rightsided_pe': data[3] }


            self.results = pd.concat([self.results, pd.DataFrame([data])], ignore_index=True)

            if self.progressBar != None:
                self.progressBar.setValue(((i+1) / datalength) * 100)

            #print(self.results)

        print(self.results)

        
    def report(self, outputdir):

        if self.config["save-csv"]:
            #print(self.results)
            self.results.to_csv(outputdir+'/report.csv', index=False)


        if self.config["save-report"]:

            total = sum(1 for x in self.results.iterrows())
            pe = sum(1 for x in self.results['pe_present_on_image'] if x == 1)
            left_pe = sum(1 for x in self.results['leftsided_pe'] if x == 1)
            center_pe = sum(1 for x in self.results['central_pe'] if x == 1)
            right_pe = sum(1 for x in self.results['rightsided_pe'] if x == 1)

            dataset = self.results.values.tolist()

            generate_report(
                outputdir=outputdir,
                name='XXXXXX', 
                total = total,
                pe = pe,
                left = left_pe,
                center = center_pe,
                right = right_pe,
                dataset = dataset 
            )

        #reset dataframe
        self.results = pd.DataFrame(columns=['image','pe_present_on_image','leftsided_pe','central_pe','rightsided_pe'])

if __name__ == "__main__":
    from filemanager import FileManager
    from sequence import DCMSequence
    from preprocessor import Preprocessor
    path = '/home/raffique/Desktop/train/6897fa9de148'
    fm = FileManager()
    files = fm.tree(path)
    sq = DCMSequence(files)
    files = sq.get_sq()
    ai = PulmonaryEmbolismDetector()
    ai.config['lungs-localizer'] = False
    ai.data(inputdir=files, outputdir="/home/raffique/Documents/")



    
