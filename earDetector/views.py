from django.shortcuts import render
from django.contrib import messages

from earDetectionWebApp.settings import BASE_DIR
from earDetector.earDetect import earDetect
from earDetector.forms import PhotoUpload

from skimage import  io, filters
from django.contrib.auth.decorators import login_required

import io
import glob
import os

@login_required(login_url="../login/")
def home(request):
    xmls = get_all_xmls()
    return render(request, "earDetect.html",{'xmls':xmls})


@login_required(login_url="../login/")
def detect(request):
    if request.method == 'POST':
        form = PhotoUpload(request.POST, request.FILES)
        if form.is_valid():
            #image = Image(image=request.FILES['image'])
            image = request.FILES['image']
            data = image.read()
            image.close()
            xml = form.clean_field('xml')
            ellipse_find = form.clean_field('ellipse_find')
            do_rotation = form.clean_field('do_rotation')
            rotation = form.clean_field('rotation')

            detector = earDetect(xml)
            (images_url,a) = detector.detect_from_bytes(data, image.name, ellipse=ellipse_find, rotation=(do_rotation, rotation))

            print('Im;'+str(images_url))
            print('A:'+str(a))

            if not images_url:
                messages.warning(request,"Ziadne ucho nebolo najdene!", fail_silently=True)
            else:
                messages.success(request, "Ucho bolo najdene! Rotacia: "+str(a) + "°",fail_silently=True)

            return render(request, 'earDetect.html', {'images': images_url,
                                                      'xmls': get_all_xmls()})

        else:
            print('not valid')
            form = PhotoUpload()


    return None

@login_required(login_url="../login/")
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

def get_all_xmls():
    all_xmls = glob.glob(BASE_DIR + '/earDetector/xml/*.xml')
    xmls = list()
    for one_xml in all_xmls:
        xmls.append((os.path.basename(one_xml), one_xml))
    return xmls
