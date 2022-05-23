# PULMONARY EMBOLISM DETECTOR

University of the West Indes Mona Jamaica

Faculty of Science and Technology

COMP3901 Capstone finalproject 

Classification of Pulmonary Embolism

**The preprocessing and training sections can be skipped if retraining desired**

#Preprocessing of Dataset 
In the prepocessing stage; a 2.5D image transformation technique was applied to our dataset,
which is combining 3 grayscale images that are direct neigbours in the sequence of images scan. they are combined in the same layer format of of an RGB image and this results in a image  that simulates having depth rathe than a flat appearance. introudcing depth to the images gives the neural network more information to learn.

The Following notebooks split up the data into 7 parts and also creates a csv keeping track of them
**csv-creator-1.ipynb**
**csv-creator-2.ipynb**
**csv-creator-3.ipynb**
**csv-creator-4.ipynb**
**csv-creator-5.ipynb**
**csv-creator-6.ipynb**
**csv-creator-7.ipynb**


#Training models

**Lungs Segmenter**
Notebook: training/lungs-u-net.ipynb
Dataset for training: https://www.kaggle.com/datasets/kmader/finding-lungs-in-ct-data

**Pulmonary Embolism CNN classifier model**
Notebook: training/pe-cnn.ipynb
https://www.kaggle.com/competitions/rsna-str-pulmonary-embolism-detection/data

**Pulmonary Embolism Resnet50 classifier model**
Notebook: training/pe-resnet50.ipynb
https://www.kaggle.com/competitions/rsna-str-pulmonary-embolism-detection/data

**Pulmonary Embolism Resnet50 location classifier model**
Notebook: training/pe-resnet50.ipynb
https://www.kaggle.com/competitions/rsna-str-pulmonary-embolism-detection/data


#Starting the GUI Aplication

**Links to models:**
https://drive.google.com/file/d/1ZtL9nWUm_Z6sVve9f6hddyDu9WqUma5n/view?usp=sharing

The trained model and weights are too big to store in the repository.
1.Download the zip file
2.Extract the folder model containing the trained models
3.place the folder "model" in the root of this directory

**pip install -r requirements.txt**

**run main.py**

