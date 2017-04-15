import cv2
import glob
import os
from earTrainer.tester.Comparator import Comparator
from earTrainer.main.utils import PropertyUtils
from sys import platform

from shutil import copyfile

cv2.ocl.setUseOpenCL(False)

class Tester:

    def __init__(self, xml_ear_file = '', descriptor_name = 'descriptor.txt', trainer_name = 'default', custom=False,samples_dir='samples/'):
        self.root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        properties = PropertyUtils()

        # docker props
        if platform == 'linux':
            propsmain = properties.get_all('docker')
        else:
            propsmain = properties.get_all('main')

        self.custom = custom
        self.root_dir = propsmain.get('testerdir')

        self.xmls_dir = os.path.join(self.root_dir,'xmls/')
        if not os.path.exists(self.xmls_dir):
            os.makedirs(self.xmls_dir)

        self.detector = None
        self.xml_file = ''
        self.xml_ear_file = xml_ear_file

        if xml_ear_file is not '' and not custom:
            #copy to xmls dir
            new_name = trainer_name+'.xml'
            copyfile(xml_ear_file,os.path.join(self.xmls_dir,new_name))
            self.xml_file = os.path.join(self.xmls_dir,new_name)
            #os.rename(os.path.join(self.xmls_dir,'cascade.xml'),self.xml_file)
            self.detector = cv2.CascadeClassifier(self.xml_file)
            self.result_dir = os.path.join(self.root_dir, 'results/')
        else:
            self.detector = cv2.CascadeClassifier(self.xml_ear_file)


        self.result_file_name = 'results.txt'
        self.result_ear_not_found = 'not_found.txt'

        self.testing_samples = os.path.join(self.root_dir,samples_dir)
        self.descriptor = descriptor_name
        self.penalty = 0
        self.comparator = Comparator(samplesDir=self.testing_samples)

    def start(self):
        print('#####################')
        print('Running XML Tester')

        testing_images = glob.glob(self.testing_samples + '/*.jpg')

        # na porovnavanie regionov ( IoU )

        results = []
        not_found = 0

        # create dir to result ( based on xml name )
        if not self.custom:
            result_file_dir = os.path.join(self.result_dir, self.xml_ear_file.split('.')[0]+'/')
            print('Result file dir ',result_file_dir)
            if not os.path.exists(result_file_dir):
                print('creating')
                os.makedirs(result_file_dir)
            result_file_dir = os.path.join(result_file_dir,self.result_file_name)
            ##
            print('Result file dir ',result_file_dir)

            with open(result_file_dir,'w+') as result_file:
                for one in testing_images:
                    self.detect(one,not_found,results,result_file)

                # print final result
                if not sum(results) == 0:
                    result = sum(results) / len(results)
                else: result = 0

                result_file.write("Final Result: {0}".format(result))
        else:
            print('CUSTOM')
            print(self.testing_samples)
            for one in testing_images:
                print(one)
                self.detect(one, not_found, results)

            # print final result
            if not sum(results) == 0:
                result = sum(results) / len(results)
            else:
                result = 0

        print('#### END #####')
        print('Final Result IoU: ', result)
        print('Not found: {0}/{1}'.format(not_found,len(results)))

        return result


    def detect(self,one, not_found, results,result_file=None):
        img = cv2.imread(one)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        rect = None

        # detect ear
        if self.detector is not None:
            ears = self.detector.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5,
                                                  minSize=(1, 1), maxSize=(1000, 1000), flags=cv2.CASCADE_SCALE_IMAGE)
            for (x, y, w, h) in ears:
                rect = (x, y, x + w, y + h)
                print('X: {0} Y: {1} W: {2} H: {3} '.format(x, y, w, h))
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # TODO: implement IoS
        print('Comparing...')

        if rect is None:
            not_found += 1

        iou = self.comparator.compareOne(os.path.basename(one), rect, False)

        if iou is -1:
            iou = self.penalty

        line = "{0} {1}\n".format(one, iou)
        if result_file:
            result_file.write(line)
        results.append(iou)

        if iou == -1:
            print('Img {0} not found. Try to Mark it first'.format(one))
            not_found += 1


    def test(self):
        testing_images = glob.glob(self.testing_samples + '/*.jpg')
        one = testing_images[-1]
        img = cv2.imread(one)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        orb = cv2.ORB_create()
        kp = orb.detect(gray, None)
        kp, descriptors = orb.compute(gray, kp)

        cv2.drawKeypoints(img, kp, color=(0, 255, 0), flags=0, outImage=img)
        cv2.imshow('ORB keypoints', img)
        cv2.waitKey()