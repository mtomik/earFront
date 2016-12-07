from django.shortcuts import render

from earDetectionWebApp.settings import BASE_DIR
from earDetector.forms import PhotoUpload
from earDetector.models import Image
from earDetectionWebApp import settings
import numpy as np
import cv2
from sklearn import datasets
from skimage import data, io, filters

def home(request):
    return render(request, "earDetect.html")


def detect(request):
    if request.method == 'POST':
        form = PhotoUpload(request.POST, request.FILES)
        if form.is_valid():
            print('image received')
            #image = Image(image=request.FILES['image'])
            image = request.FILES['image']
            data = image.read()
            image.close()
            print(BASE_DIR)
            # TODO: Add xml classif
            ear_detector = cv2.CascadeClassifier(BASE_DIR+'/earDetector/xml/haarcascade_frontalface_default.xml')

            # from raw data to numPy image
            np_arr = np.fromstring(data, np.uint8)
            img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            ears = ear_detector.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in ears:
                print('Ear found! x: {0} y: {1} w: {2} h: {3}'.format(x,y,w,h))
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)


            # show debug image
            # cv2.imshow('test',edges)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            imageUrl = 'media/images/'+image.name
            cv2.imwrite(imageUrl,img)
            # image.image = edges
            # image.save()
            # cv2.im

            return render(request, 'earDetect.html', {'image':'/'+imageUrl})
        else:
            form = PhotoUpload()

        return None


def detectSciKit(request):
    if request.method == 'POST':
        form = PhotoUpload(request.POST, request.FILES)
        if form.is_valid():
            print('image received')
            image = request.FILES['image']
            dataI = image.read()
            print(type(dataI))
            image.close()
            print(BASE_DIR)


            imageUrl = 'media/images/' + image.name
            dataI = io.imread(imageUrl)

            edges = filters.sobel(dataI)
            io.imsave(imageUrl)


            return render(request, 'earDetect.html', {'image':'/'+imageUrl})
        else:
            form = PhotoUpload()

        return None
