""" 
Example of data generated from filemanger for dcmsequence to process
[
    {
        'inputdir': 'xxxxx/yyyy/zzzz',
        'traverse': 'aa/bb/cc/',
        'length': 5,
        'fromzip': False,
        'haszip': False,
        'hasdcm': True,
        'sequence': [
            {
                'filename' : 'ajhdjocs.dcm',
                'data' : 'path to dcm file or lambda fucntion extractig file from zip then read by dicomBytesIO',
            },
            {
                'filename' : 'ajhdjocs.dcm',
                'data' : 'path to dcm file or lambda fucntion extractig file from zip then read by dicomBytesIO',
            },
            {
                'filename' : 'ajhdjocs.dcm',
                'data' : 'path to dcm file or lambda fucntion extractig file from zip then read by dicomBytesIO',
            }
        ]
    },
    .....,
    .....,
    .....,
]
"""
import pydicom as di
from zipfile import ZipFile as zf
from pydicom.filebase import DicomBytesIO

class DCMSequence:
    MINIMUM = 30
    def __init__(self, sequences):

        
        self.sequences = sequences
        self.validate()

    def validate(self):

        def isdcm_and_seq(file):
            res = False
            try:
                file = di.dcmread(file)
                res = int(file.InstanceNumber) > -1
            except:
                pass
            return res

        #filter dictorinaries that dont meet criteria of having dcm and being an instance in a sequence
        self.sequences = [ 
            sq 
            for sq in self.sequences 
            if sq['hasdcm'] == True 
            and sq['length'] >= DCMSequence.MINIMUM
            ]

        
        #fliter elements that are not apart of a dcm slices in the sequences 
        copy = self.sequences
        for i in range(len(copy)):
            temp = []
            for j in range(len(copy[i]['sequence'])):
                if copy[i]['fromzip']:
                    #if isdcm_and_seq(copy[i]['sequence'][j]['data']()): # this way is slower
                    if isdcm_and_seq(DicomBytesIO( zf(copy[i]['inputdir']).read( copy[i]['sequence'][j]['data'] ))):
                        temp.append(copy[i]['sequence'][j])
                else:
                    if isdcm_and_seq( copy[i]['sequence'][j]['data'] ):
                        temp.append(copy[i]['sequence'][j])


            self.sequences[i]['sequence'] = temp

        #Sort the sequences in numerical order by instance number

        for i in range(len(self.sequences)):
            if self.sequences[i]['fromzip']:
                #self.sequences[i]['sequence'].sort(key= lambda x: int(di.dcmread(x['data']()).InstanceNumber)) #this way is slower
                self.sequences[i]['sequence'].sort(key= lambda x: int(di.dcmread(DicomBytesIO(zf(self.sequences[i]['inputdir']).read( x['data'] ))).InstanceNumber))
            else:
                self.sequences[i]['sequence'].sort(key= lambda x: int(di.dcmread(x['data']).InstanceNumber))
                
            self.sequences[i]['length'] = len(self.sequences[i]['sequence'])

    def get_sq(self):
        return self.sequences


if __name__ == "__main__":
    from filemanager import FileManager
    fm = FileManager()
    path1 = '/home/raffique/Desktop/BERRY_D'
    path2 = ['/home/raffique/Desktop/BERRY_D.zip']
    files = fm.tree(path2)
    dcmsq = DCMSequence(files)
    print(len(dcmsq.get_sq()))
    