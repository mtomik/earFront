import cv2
from django.shortcuts import render
from earDetector.forms import PhotoUpload
from earDetector.models import Image
from earDetectionWebApp import settings
import numpy as np


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

            np_arr = np.fromstring(data, np.uint8)
            img_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            edges = cv2.Canny(img_np,100,200)

            # show debug image
            # cv2.imshow('test',edges)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            imageUrl = 'media/images/'+image.name
            cv2.imwrite(imageUrl,edges)

            # image.image = edges
            # image.save()
            # cv2.im

            return render(request, 'earDetect.html', {'image':'/'+imageUrl})
        else:
            form = PhotoUpload()

        return None
