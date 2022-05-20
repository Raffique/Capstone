# Capstone

# PULMONARY EMBOLISM DETECTOR

Capstone finalproject implementation of nueural networks:

```
```

RSNA-STR-PE DATASET FROM KAGGLE

```python
classes = ['{}_pe_present_on_image',
 '{}_negative_exam_for_pe',
 '{}_indeterminate',
 '{}_chronic_pe',
 '{}_acute_and_chronic_pe',
 '{}_central_pe',
 '{}_leftsided_pe',
 '{}_rightsided_pe',
 '{}_rv_lv_ratio_gte_1',
 '{}_rv_lv_ratio_lt_1',
]
```

UNZIP file from GITHUB

then download models
https://drive.google.com/file/d/1gT-K-Ov3RNtK_iZi6P440CtAZxZevLuY/view?usp=sharing

To run our program first the required models are needed and need to be downloaded and placed in the following folders
link to models


from the unzip file
----------------------------------------------------
models->RESNET50->version 2->results(2)->model.h5

to the foler
/present/
----------------------------------------------------
models->RESNET50->version 2->results(2)->weights.h5


to the folder
/present/
----------------------------------------------------
models->RESNET50 for locations->version 2->results(1)->best_model.h5

to the folder
/location/
----------------------------------------------------
models->RESNET50 for locations->version 2->results(1)->weights.h5

to the folder
/location/
---------------------------------------------------
models->UNET for lungs->results(2)->model.h5

to the folder
/lungs/
---------------------------------------------------
models->UNET for lungs->results(2)->model-weights.h5

to the folder
/lungs/
---------------------------------------------------

then 
pip imstall -r requirements



then to run the GUI application 
python main.py
