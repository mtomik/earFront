import os
import glob
import cv2
from ast import literal_eval
from earTrainer.main.utils import PropertyUtils
from sys import platform

class Comparator(object):

    def __init__(self):
        self.root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        properties = PropertyUtils()

        # docker props
        if platform == 'linux':
            propsmain = properties.get_all('docker')
        else:
            propsmain = properties.get_all('main')

        self.root = propsmain.get('testerdir')

        self.results = os.path.join(self.root,'results/')
        self.descriptor = os.path.join(self.root,'descriptor.txt')
        self.samples = os.path.join(self.root, 'samples/')



    # prienik dvoch oblasti
    def bb_intersection_over_union(self, boxA, boxB):
        xA = max(boxA[0], boxB[0])
        yA = max(boxA[1], boxB[1])
        xB = min(boxA[2], boxB[2])
        yB = min(boxA[3], boxB[3])

        # compute the area of intersection rectangle
        interArea = (xB - xA + 1) * (yB - yA + 1)

        # compute the area of both the prediction and ground-truth
        # rectangles
        boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
        boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)

        # compute the intersection over union by taking the intersection
        # area and dividing it by the sum of prediction + ground-truth
        # areas - the interesection area
        iou = interArea / float(boxAArea + boxBArea - interArea)

        # return the intersection over union value
        return iou

    def compareOne(self, img_name, rect, show):
        print('Comparing {0} {1}'.format(img_name,rect))

        with open(self.descriptor) as desc_file:
            found = False

            for line in desc_file:
                if img_name == line.split()[0]:
                    found = True
                    print('img found ',line)
                    rect_to_compare = line.split(' ',1)[1].strip()
                    print('rect ',rect_to_compare)

                    if rect_to_compare == 'negative':
                        # na fotke bez ucha detektor nenasiel ziadne ( spravne )
                        if rect is None:
                            print("Match!")
                            return 1
                        # detektor nasiel ucho tam kde nemalo byt
                        else:
                            print('Bad ear found by detector.')
                            return -1
                    # detektor nenasiel nic
                    elif rect is None:
                        print('No ear found by detector.')
                        return -1

                    rect_to_compare = literal_eval(rect_to_compare)

                    print('rect resolved: ',rect)
                    # rob IoU
                    iou = self.bb_intersection_over_union(rect_to_compare,rect)
                    print('IoU: ',iou)

                    if show:
                        img_to_show = os.path.join(self.samples,line.split(' ',1)[0])
                        img = cv2.imread(img_to_show)
                        # x,y   x+w, y+h
                        cv2.rectangle(img,(rect_to_compare[0],rect_to_compare[1]),(rect_to_compare[2],rect_to_compare[3]),(0,255,0),2)
                        cv2.rectangle(img,(rect[0],rect[1]),(rect[2],rect[3]),(255,0,0),2)
                        cv2.imshow('img',img)
                        cv2.waitKey(0)


                    return iou

            if not found:
                return -1



    def compareAll(self):
        images = glob.glob(self.samples + '/*.jpg')

        for one in images:
            img = cv2.imread(one)


