import cv2
import numpy as np
from imutils.object_detection import non_max_suppression
from earDetectionWebApp.settings import MEDIA_URL, BASE_DIR, MEDIA_ROOT
import io
from PIL import Image
import imutils
import os

class earDetect:

    MAX_WIDTH = 300
    xml_file = ''
    detector = None

    def __init__(self, xmlfile):
        self.xml_file = xmlfile
        self.detector = cv2.CascadeClassifier(self.xml_file)


    def resize(self,pil_img):
        w_percent = (self.MAX_WIDTH / float(pil_img.size[0]))
        hsize = int((float(pil_img.size[1]) * float(w_percent)))
        print('hSize: ' + str(hsize))
        pil_img.thumbnail((self.MAX_WIDTH, hsize), Image.ANTIALIAS)
        return np.array(pil_img)

    def detect(self,img,name, ellipse=True, rotation=(True,15)):
        result_images = list()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

        if rotation[0]:
            return self.detect_with_rotation(img, gray, result_images, ellipse, name, rotation[1])

        return self.detect_sequence(img, gray, result_images, ellipse, name)


    def detect_from_bytes(self,data,name, ellipse=True, rotation=(True,15)):
        b_data = np.fromstring(data, np.uint8)
        img = Image.open(io.BytesIO(b_data)).convert('RGB')
        img = self.resize(img)

        #np_arr = np.fromstring(image, np.uint8)
        #img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        return self.detect(img,name,ellipse,rotation)
        # ears = self.detector.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5,
        #                                  minSize=(1, 1), maxSize=(1000, 1000), flags=cv2.CASCADE_FIND_BIGGEST_OBJECT)
        #
        # if ears is not None:
        #     print('Ear found by Cascade Detector!')
        #     rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in ears])
        #     pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)
        #
        #     # draw the final bounding boxes
        #     for (xA, yA, xB, yB) in pick:
        #         cv2.rectangle(img, (xA, yA), (xB, yB), (0, 255, 0), 2)
        #
        #     print("[INFO] : {} original boxes, {} after suppression".format(
        #         len(rects), len(pick)))
        #
        #     if len(pick) > 0 :
        #         img_url = self.save_image(img,name)
        #         result_images.append(img_url)
        #
        #         if ellipse:
        #             pick = self.return_biggest(pick)
        #             only_ear = gray[pick[1]:pick[3], pick[0]:pick[2]]
        #             img = self.contour_match(only_ear)
        #             img2_url = self.save_image(img,'contour.jpg')
        #             result_images.append(img2_url)
        #
        #
        #         #TODO: aplikovat background substract
        #         return result_images
        #     else : return None
        #
        #
        #     # cv2.imshow(one, img)
        # else:
        #     return None

    def detect_sequence(self,orig,gray,result_images,ellipse,name):
        ears = self.detector.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5,
                                              minSize=(1, 1), maxSize=(1000, 1000),
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
                result_images.append(img_url)

                if ellipse:
                    pick = self.return_biggest(pick)
                    only_ear = gray[pick[1]:pick[3], pick[0]:pick[2]]
                    img = self.contour_match(only_ear)
                    img2_url = self.save_image(img,'contour.jpg')
                    result_images.append(img2_url)


                #TODO: aplikovat background substract
                return result_images
        return None


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

        gray = cv2.GaussianBlur(img, (11, 11), 0)
        gray = cv2.medianBlur(gray, 11)

        # gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        #                              cv2.THRESH_BINARY, 11, 2)

        gray = cv2.erode(gray, None, iterations=3)
        gray = cv2.dilate(gray, None, iterations=4)

        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 11, 1)
        kernel = np.ones((3, 3), np.uint8)
        closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=4)

        im2, cnts, hierarchy = cv2.findContours(closing,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        biggest = None
        biggest_area = 0
        for one in cnts:
            area = cv2.contourArea(one)
            print(area)

            if len(one) > 5:
                if biggest_area < area:
                    biggest_area = area
                    biggest = one

        ellipse = cv2.fitEllipse(biggest)
        cv2.ellipse(normal, ellipse, (255, 0, 0), 2)
        return normal


    def detect_rotate(self,img,gray,result_images,ellipse,name,angle):
        rotated = imutils.rotate_bound(gray, angle)
        imgs = self.detect_sequence(img, rotated, result_images, ellipse, name)
        if imgs:
            print('Ear found on angle: ' + str(angle))
            return imgs, angle

    def detect_with_rotation(self,orig,gray,result_images,ellipse,name,angle):
        for a in range(0,180,angle):
            print('Rotating.. Angle: '+str(a))
            imgs = self.detect_rotate(orig,gray,result_images,ellipse,name,a)
            if imgs:
                print('Ear found on angle: ' + str(a))
                return imgs, a

            if a > 0:
                imgs = self.detect_rotate(orig, gray, result_images, ellipse, name, -a)
                if imgs:
                    print('Ear found on angle: ' + str(a))
                    return imgs, a

        return None







