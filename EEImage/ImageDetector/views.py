from django.shortcuts import render

from django.core.files.storage import FileSystemStorage

import os
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import cv2
import numpy as np
from tensorflow.keras.models import load_model

final_model = load_model('/Users/oreadeniyi/Desktop/multiimageclassifier3.h5')
# Create your views here.

def index(request):
    context={'a':1}
    return render(request,'index.html',context)

def predictElement(request):
    print(request)
    print(request.POST)
    print(request.FILES['filePath'])
    fileObj = request.FILES['filePath']
    fs = FileSystemStorage()
    filePathName=fs.save(fileObj.name,fileObj)
    filePathName= fs.url(filePathName)
    testimage = '.'+filePathName

    img = image.load_img(testimage,target_size=(256,256))
    resize = image.img_to_array(img)
    resize = resize/255;
    resize = resize.reshape(1,256,256,3)

    image_class_final = np.argmax(final_model.predict(resize))
   

    def numbers_to_label(argument):
    
        switcher = {
        0: "Capacitor",
        1: "Inductor",
        2: "Resistor",
        3: "BJT",
        4: "Diode",
        5: "Dependent Current Source",
        6: "Dependent Voltage Source",
        7: "Ground",
        8: "Current Source",
        9: "MOSFET",
        10: "OP-AMP",
        11: "Voltage Source"

        }
      # get() method of dictionary data type returns
    # value of passed argument if it is present
    # in dictionary otherwise second argument will
    # be assigned as default value of passed argument
        return switcher.get(argument, "nothing")


    print(numbers_to_label(image_class_final))


    predictedElement = numbers_to_label(image_class_final)
    context={'filePathName':filePathName,'predictedElement':predictedElement}
    return render(request,'index.html',context) 

def viewDataBase(request):
    listOfImages = os.listdir('./media/')
    listofImagesPath = ['./media/'+i for i in listOfImages]
    context = {'listofImagesPath':listofImagesPath}
    return render(request,'viewDB.html',context)

