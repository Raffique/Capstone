import os
from zipfile import ZipFile as zf, is_zipfile as is_zf
from pydicom.errors import InvalidDicomError
import pydicom as di
from pydicom.filebase import DicomBytesIO


class FileManager:
    def __init__(self):
        self.progress = 0
        self.inputdir = ''
        self.outputdir = ''
        self.folders = []

    def is_dcmfile(self, file:str):
        """
        Check whether a given file is of type DICOM
        # the original try statement to test if  file is a dcm-file slows down the program
        # just testing for file extension .dcm or no extension works faster

        :param file: path to the file to identify
        :type file: str

        :return: True if the file is DICOM, False otherwise
        :type: bool

        """

        """ try:
            di.dcmread(file)
        except InvalidDicomError:
            return False
        return True  """

        return file[-4:] == ".dcm" or len(file.split('.')) == 1

    def unzip(self, file:str):
        folders = {}
        worker = zf(file)
        zfiles = worker.namelist()
        #===========================================================================
        #this creates a diectionary that keys are directory location strings
        #and values area list that contains dictionaries   
        for zfile in zfiles:
            #if statement to filter out folders
            if zfile[-1] != "/":
                traverse_path = zfile[:-1*len(zfile.split('/')[-1])]
                filename = zfile[len(traverse_path):]
                if traverse_path not in list(folders.keys()):
                    folders[traverse_path] = []
                #data = {'filename': filename, 'data': lambda :  DicomBytesIO(worker.read(zfile))} #this way slows down program
                data = {'filename': filename, 'data': zfile}
                folders[traverse_path].append(data)
        #===========================================================================
        #this converts the dictionary of data to a list of data
        folders = [
            {
                'inputdir': file,
                'traverse' : key,
                'sequence': val,
                'length': len(val),
                'haszip': False,
                'fromzip': True,
                'hasdcm' : True in [self.is_dcmfile(el['filename']) for el in val]
            }
            for key, val in folders.items()
        ]

        return folders


    def is_zipfile(self, file:str):

        if is_zf(file):
            files = self.unzip(file)
            return True, files
        
        return False, None

    def tree(self, dir):
        """
        :return: a list of dictionaries for each folder and subfolder contents, path, length, has-a-zip-file and has-a-dcm-file and also input string
        :type: list, str

        """
        #removes last stroke cuz functions perform without it

        global lst
        lst = [] #stores a unifide list of all files
        
        def helper(path):
            sub_folder = []
            hasdcm = False
            haszip = False
            traverse_path = ''
            elements = os.listdir(path) #list all elements in folder
            for el in elements:
                full_path = path+'/'+el #store the absolaute path
                traverse_path = full_path[len(dir)+1 : -1*len(el)] #path traversed between input dir and filename
                filename =  el #filename
                if not os.path.isdir(full_path):
                    global lst 
                    lst += [ filename ] #removes inital directory path from file
                    haszip, files = self.is_zipfile(full_path)
                    if files != None:
                        pass
                        self.folders += files
                    hasdcm = self.is_dcmfile(full_path)
                    sub_folder.append({'filename': filename, 'data': full_path})
                else:
                    sub_folder.append({'filename': filename+'/', 'data': full_path+'/'})
                    helper(full_path)
                    
            #self.folders.append({'inputdir': path[:-1*len(traverse_path) +1], 'traverse': traverse_path, 'sequence': sub_folder, 'length': len(sub_folder), 'fromzip': False, 'haszip': haszip, 'hasdcm': hasdcm})
            self.folders.append({'inputdir': dir, 'traverse': traverse_path, 'sequence': sub_folder, 'length': len(sub_folder), 'fromzip': False, 'haszip': haszip, 'hasdcm': hasdcm})

        if os.path.isdir(str(dir)):
            if dir[-1] == '/' and len(dir) != 1:
                dir = dir[:-1]
            helper(dir)
        
        elif type(dir) == list:
            for zipfile in dir:
                self.folders += self.unzip(zipfile)

        folders = self.folders

        self.folders = []

        return folders



if __name__ == "__main__":

    #path1 = '/home/raffique/Desktop/BERRY_D'
    path1 = '/home/raffique/Desktop/train/0cee26703028/bac7becd2970'
    fm = FileManager()
    files = fm.tree(path1)# tree function dosnt like '/' at the end of it
    i = 0
    #print(files)
    print("inputdir --> {}".format(files[i]['inputdir']))
    print("traverse --> {}".format(files[i]['traverse']))
    for el in files[i]['sequence']:
        print(el)
   

    """ path2 = ['/home/raffique/Desktop/BERRY_D.zip']
    #path2 = 'app.zip'
    fm = FileManager()
    files = fm.tree(path2)
    i = 0
    print(files[i]['inputdir'])
    print(files[i]['traverse'])
    print(files[i]['length'])
    print(files[i]['hasdcm'])
    for el in files[i]['sequence']:
        print(el) """