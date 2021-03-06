import cv2
import numpy as np
from imutils.object_detection import non_max_suppression
from earDetectionWebApp.settings import MEDIA_URL, BASE_DIR, MEDIA_ROOT,properties

import io
from PIL import Image
import imutils
import os
import time

class earDetectParams():
    def __init__(self,data,name, ellipse=True, rotation=(True,15)):
        self.data = data
        self.name = name
        self.ellipse = ellipse
        self.rotation = rotation

class earDetect:

    MAX_WIDTH = 500
    xml_file = ''
    detector = None

    def __init__(self, xmlfile,type):
        self.detector = cv2.CascadeClassifier(os.path.join(properties.get('testerdir'),'xmls',xmlfile))
        self.equalizer = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(4, 4))
        self.result_images = list()
        self.type = type

    def resize(self,pil_img):
        w_percent = (self.MAX_WIDTH / float(pil_img.size[0]))
        hsize = int((float(pil_img.size[1]) * float(w_percent)))
        print('hSize: ' + str(hsize))
        pil_img.thumbnail((self.MAX_WIDTH, hsize), Image.ANTIALIAS)
        return np.array(pil_img)


    def detect_from_bytes(self,params:earDetectParams):
        b_data = np.fromstring(params.data, np.uint8)
        img = Image.open(io.BytesIO(b_data)).convert('RGB')
        t = time.time()

        #np_arr = np.fromstring(image, np.uint8)
        #img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        result = self.detect(img,params.name,params.ellipse,params.rotation)
        end = time.time()
        print('Time:',end-t)
        return result

    def detect(self,img,name, ellipse=True, rotation=(True,15)):

        img = self.resize(img)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

        gray = self.equalizer.apply(gray)

        if rotation[0]:
            return self.detect_with_rotation(img, gray, ellipse, name, rotation[1])

        return self.detect_sequence(img, gray, ellipse, name),0



    def detect_sequence(self,orig,gray,ellipse,name):
        ears = self.detector.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5,
                                              minSize=(50, 50), maxSize=(1000, 1000),
                                              flags=cv2.CASCADE_FIND_BIGGEST_OBJECT)
        if ears is not None:
            print('Ear found by Cascade Detector!')
            rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in ears])
            pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

            # draw the final bounding boxes
            for (xA, yA, xB, yB) in pick:
                cv2.rectangle(orig, (xA, yA), (xB, yB), (0, 255, 0), 2)

            print("[INFO] : {} original boxes, {} after suppression".format(
                len(rects), len(pick)))

            if len(pick) > 0 :
                img_url = self.save_image(orig,name)
                self.result_images.append(img_url)

                if ellipse:
                    pick = self.return_biggest(pick)
                    only_ear = gray[pick[1]:pick[3], pick[0]:pick[2]]
                    img,ellipse_shape = self.contour_match(only_ear)
                    img2_url = self.save_image(img,'contour.jpg')
                    self.result_images.append(img2_url)

                    # cut everything outside ellipse
                    img = self.cut_and_rotate(only_ear,ellipse_shape)
                    img3_url = self.save_image(img,'contour_cut.jpg')
                    self.result_images.append(img3_url)

                return self.result_images
        return None

    def cut_and_rotate(self,img, ellipse):
        mask = np.zeros_like(img)
        cv2.ellipse(mask, ellipse, (255, 255, 255), -1)
        cut = np.bitwise_and(img, mask)
        angle = ellipse[2]
        print(angle)
        if angle < 60:
            angle -= 180
        angle = 180 - angle

        return imutils.rotate_bound(cut, angle)



    def save_image(self,data, name):
        image_url = os.path.join(MEDIA_ROOT,'images/',name)
        print(image_url)
        cv2.imwrite(image_url, data)
        return os.path.join('/',MEDIA_URL,'images/',name)

    def return_biggest(self,rects):
        return self.sort_rects(rects)[0][1]

    def sort_rects(self,rects):
        result = list()
        for rect in rects:
            result.append(((rect[3] - rect[1]) * (rect[2] - rect[0]), rect))
        result.sort(reverse=True)
        return result

    def contour_match(self,img):
        normal = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

        gray = cv2.medianBlur(img, 9)

        kernel = np.ones((2,2),np.uint8)
        gray = cv2.erode(gray, kernel, iterations=4)
        gray = cv2.dilate(gray, kernel, iterations=4)

        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 7, 1)
        self.result_images.append(self.save_image(thresh,'0.jpg'))

        kernel = np.ones((3, 3), np.uint8)
        closing = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
        self.result_images.append(self.save_image(closing,'1.jpg'))

        kernel = np.ones((2, 2), np.uint8)
        closing = cv2.dilate(closing, kernel, iterations=1)
        self.result_images.append(self.save_image(closing,'bef.jpg'))

        kernel = np.ones((3, 3), np.uint8)
        closing = cv2.morphologyEx(closing, cv2.MORPH_CLOSE, kernel, iterations=5)
        self.result_images.append(self.save_image(closing,'after.jpg'))

        im2, cnts, hierarchy = cv2.findContours(closing, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        biggest = self.get_biggest_cnt(cnts)
        cv2.drawContours(closing, [biggest], 0, (255, 255, 255), -1)
        self.result_images.append(self.save_image(closing,'fill.jpg'))


        kernel = np.ones((5, 5), np.uint8)
        closing = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel, iterations=4)
        self.result_images.append(self.save_image(closing,'test.jpg'))
        # shift
        offset = (0,0)
        if self.type is 'lave':
                offset = (-7,0)

        im2, cnts, hierarchy = cv2.findContours(closing,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE,offset=offset)
        biggest = self.get_biggest_cnt(cnts)
        ellipse = cv2.fitEllipse(biggest)
        cv2.ellipse(normal, ellipse, (255, 0, 0), 2)
        return normal,ellipse


    def detect_rotate(self,img,gray,ellipse,name,angle):
        rotated = imutils.rotate_bound(gray, angle)
        imgs = self.detect_sequence(img, rotated, ellipse, name)
        if imgs:
            print('Ear found on angle: ' + str(angle))
            return imgs

    def detect_with_rotation(self,orig,gray,ellipse,name,angle):
        for a in range(0,180,angle):
            print('Rotating.. Angle: '+str(a))
            imgs = self.detect_rotate(orig,gray,ellipse,name,a)
            if imgs:
                print('Ear found on angle: ' + str(a))
                return (imgs, a)

            if a > 0:
                imgs = self.detect_rotate(orig, gray, ellipse, name, -a)
                if imgs:
                    print('Ear found on angle: ' + str(a))
                    return (imgs, a)

        return None

    def get_biggest_cnt(self,cnts):
        biggest = None
        biggest_area = 0
        for one in cnts:
            area = cv2.arcLength(one, True)

            if len(one) > 5:
                if biggest_area < area:
                    biggest_area = area
                    biggest = one
        return biggest










