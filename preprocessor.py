
from skimage.transform import resize

import pydicom as di
from pydicom.errors import InvalidDicomError
import numpy as np
from PIL import Image 
import os
from zipfile import ZipFile as zf
from pydicom.filebase import DicomBytesIO

import matplotlib.pyplot as plt

from keras.models import Model, load_model

"""
key: sequence -> list of dictionary values below are added in the lungs localizer
    key: white
    key: whitemax
    key: filter

key:lungs -> list of dictionary in groups of three
    [img-1, img, img+1]

"""



class Preprocessor:
    def __init__(self):
        self.inputdir = ''
        self.files = []
        self.names = []
        self.thickness = 0
        self.intercept = 0
        self.slope = 0
        self.cindex = 0
        self.climit = 0
        self.lungs_segmenter = None
        self.dcmsq  = None

    #function to set lungs localizer apart of the preprocessing stage or not...set to true or false
    def set_mode(self, stat:bool, model='models/lungs/model.h5', weights='models/lungs/model-weights.h5'):
        if stat == True:
            self.lungs_segmenter = load_model(model)
            self.lungs_segmenter.load_weights(weights)
        else:
            self.lungs_segmenter = None

    #localize the lungs in the image files
    def localizer(self, files):

        res = []
        max_val = 0
        white_threshold = 600
        filter_percentage = 0.7
        filter_percentage2 = 0.6
        filter_val = 0

        #returns the predict mask numpy img and also the amount of white in the pic 
        def masker(img, w=64, h=64, threshold=200):

            #standardize the range of the dcm pixel array to 0-255
            def trans(img):
                img_2d = img.astype(float)
                img_2d_scaled = (np.maximum(img_2d,0) / img_2d.max()) * 255.0
                img_2d_scaled = np.uint8(img_2d_scaled)
                return img_2d_scaled

            img = trans(img.pixel_array)
            img = resize(img, (w,h))
            img2 = img.reshape(1,w,h,1)
            pred = self.lungs_segmenter(img2, training=False).numpy()
            pred = pred.reshape(w,h,1)
            pred = trans(pred)
            white = np.count_nonzero(np.all(pred>=[threshold], axis=2))
            return pred, white

        copy = files
        for n in range(len(files)):
            max_val =  0
            for i in range(files[n]['length']):
                pred, white = None, None

                if files[n]['fromzip']:
                    pred, white = masker( di.dcmread(DicomBytesIO( zf(files[n]['inputdir']).read( files[n]['sequence'][i]['data']))) )
                else:
                    pred, white = masker(di.dcmread(files[n]['sequence'][i]['data']))

                if max_val < white:
                    max_val = white

                copy[n]['sequence'][i]['white'] = white
            copy[n]['whitemax'] = max_val
                
                
            if copy[n]['whitemax'] < white_threshold:
                copy[n]['filter'] = copy[n]['whitemax'] * filter_percentage
            else:
                copy[n]['filter'] = copy[n]['whitemax'] * filter_percentage2


        #make a lungs key in dictionary for just lung images
        
        for i in range(len(copy)):
            sub_sq = []
            for j in range(copy[i]['length']):
                if copy[i]['sequence'][j]['white'] >= copy[i]['filter']:
                    if j == 0:
                        sub_sq.append([copy[i]['sequence'][j], copy[i]['sequence'][j], copy[i]['sequence'][j+1]])

                    elif j == copy[i]['length'] -1:
                        sub_sq.append([copy[i]['sequence'][j-1], copy[i]['sequence'][j], copy[i]['sequence'][j]])

                    else:
                        sub_sq.append([copy[i]['sequence'][j-1], copy[i]['sequence'][j], copy[i]['sequence'][j+1]])
            copy[i]['lungs'] = sub_sq
            copy[i]['length'] = len(sub_sq)
            

        return copy



    def ssf(self, dcmsq):

        self.dcmsq = dcmsq
        if self.lungs_segmenter != None:

            len1 = [x['length'] for x in self.dcmsq]
            self.dcmsq = self.localizer(self.dcmsq)
            len2 = [x['length'] for x in self.dcmsq]

            print('lung localizer activated')
            for i in range(len(len1)):
                print('Sequence {} filter from {} to {} files.'.format(i, len1[i], len2[i]))

        
        self.sqmap = [ [ 0, sq['length'] ] for sq in self.dcmsq] # [[0,669], [0,334], [0,200]] (index, limit)
        print(self.sqmap)
    

    #input a read dcm file and output img as a numpy in the PE Window default 
    def window(self, dcm, WL=100, WW=700):

        def check(x):
            #get x[0] as in int is x is a 'pydicom.multival.MultiValue', otherwise get int(x)
            if type(x) == di.multival.MultiValue:
                return int(x[0])
            else: 
                return int(x)

        intercept = check(dcm[('0028','1052')].value)
        slope = check(dcm[('0028','1053')].value)
        img = dcm.pixel_array
        img = (img*slope +intercept) #for translation adjustments given in the dicom file. 
        upper, lower = WL+WW//2, WL-WW//2
        X = np.clip(img.copy(), lower, upper)
        X = X - np.min(X)
        X = X / np.max(X)
        X = (X*255.0).astype('uint8')
        X = np.expand_dims(X, axis=2)
        return X
    
    #combine 3 numpy images
    def fusers(self, f1,f2,f3):
        ds1 = self.window(f1)
        ds2 = self.window(f2)
        ds3 = self.window(f3)

        #===================THIS SHOULD BE CORRECTED TO BEFORE CURRENT AFTER SLICE POSITIONS=====================#
        #ds = np.concatenate([ds1,ds2,ds3], axis=2)
        ds = np.concatenate([ds2,ds1,ds3], axis=2)
        """RESCALE IMAGE """
        ds = ds / 255.0 #ALWAYS REMEBER TO  RESCALE YOU DATA MODEL TO THE SAME AS YOU TRAINED IT !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
        return ds
    
    def iterator(self):

        def fd(x, y, z=0):
            if self.lungs_segmenter == None:
                return di.dcmread(self.dcmsq[x]['sequence'][y]['data'])
            else:
                return di.dcmread(self.dcmsq[x]['lungs'][y][z]['data'])

        def zd(x, y, z=0):
            if self.lungs_segmenter == None:
                return di.dcmread(DicomBytesIO( zf(self.dcmsq[x]['inputdir']).read(self.dcmsq[x]['sequence'][y]['data'])))
            else:
                return di.dcmread(DicomBytesIO( zf(self.dcmsq[x]['inputdir']).read(self.dcmsq[x]['lungs'][y][z]['data'])))

        def fdzd(x, y, z=0):
            if self.dcmsq[x]['fromzip']:
                return zd(x,y,z)
            else:
                return fd(x,y,z)

        def getname(x, y, z=1):

            #get name of input folder from absolute path
            def rooter(dir):
                if dir[-1] == '/' and len(dir) > 1:
                    dir = dir[:-1]
                if dir == '/':
                    return dir
                else:
                    return dir.split('/')[-1]

            if self.lungs_segmenter == None:
                return rooter(self.dcmsq[x]['inputdir']), self.dcmsq[x]['traverse']  + self.dcmsq[x]['sequence'][y]['filename']
            else:
                return rooter(self.dcmsq[x]['inputdir']), self.dcmsq[x]['traverse']  + self.dcmsq[x]['lungs'][y][z]['filename']



        if self.sqmap[-1][0] == self.sqmap[-1][1]:
            return False
        else:

            sqindex = 0
            sliceindex = 0

            for i in range(len(self.sqmap)):
                if self.sqmap[i][0] < self.sqmap[i][1]:
                    sliceindex = self.sqmap[i][0]
                    sqindex = i
                    break

            img = None
            if sliceindex == 0:
                if self.lungs_segmenter == None:
                    img = self.fusers(fdzd(sqindex, sliceindex), fdzd(sqindex, sliceindex), fdzd(sqindex, sliceindex+1))
                else:
                    img = self.fusers(fdzd(sqindex, sliceindex, 0), fdzd(sqindex, sliceindex, 1), fdzd(sqindex, sliceindex+1, 2))

            elif sliceindex == self.sqmap[sqindex][1] -1:
                if self.lungs_segmenter == None:
                    img = self.fusers(fdzd(sqindex, sliceindex-1), fdzd(sqindex, sliceindex), fdzd(sqindex, sliceindex))
                else:
                    img = self.fusers(fdzd(sqindex, sliceindex-1, 0), fdzd(sqindex, sliceindex, 1), fdzd(sqindex, sliceindex, 2))

            else:
                if self.lungs_segmenter == None:
                    img = self.fusers(fdzd(sqindex, sliceindex-1), fdzd(sqindex, sliceindex), fdzd(sqindex, sliceindex+1))
                else:
                    img = self.fusers(fdzd(sqindex, sliceindex-1, 0), fdzd(sqindex, sliceindex, 1), fdzd(sqindex, sliceindex+1, 2))

            root, name = getname(sqindex, sliceindex)
            sliceindex += 1
            self.sqmap[sqindex][0] = sliceindex

            return img, name, root

    def datasum(self):
        return sum(x[1] for x in self.sqmap)

    def reset(self):
        sliceindex = 0
            

if __name__ == "__main__":

    from filemanager import FileManager
    from sequence import DCMSequence

    #path = '/home/raffique/Desktop/BERRY_D'
    path = '/home/raffique/Desktop/train/0cee26703028/bac7becd2970'
    #path = ['/home/raffique/Desktop/BERRY_D.zip']
    

    fm = FileManager()
    files = fm.tree(path)
    """ i = 0
    print(files[i]['inputdir'])
    print(files[i]['traverse'])
    print(files[i]['length'])
    print(files[i]['hasdcm'])
    for el in files[i]['sequence']:
        print(el) """

    dcmsq = DCMSequence(files)
    files = dcmsq.get_sq()
    """ i = 0
    print(files[i]['inputdir'])
    print(files[i]['traverse'])
    print(files[i]['length'])
    print(files[i]['hasdcm'])
    for el in files[i]['sequence']:
        print(el) """

    preprocessor = Preprocessor()
    preprocessor.set_mode(False)
    preprocessor.ssf(files)

    fix, ax = plt.subplots(4,4)
    for i in range(4):
        for j in range(4):
            img, name, root = preprocessor.iterator()
            print("inputdir --> {} || name --> {}".format(root, name))
            ax[i,j].imshow(img)
    plt.show()

