import cv2


class earDetect:

    xmlFile = ''

    def __init__(self, xmlfile):
        self.xmlFile = xmlfile

    def showVersion(self):
        print(cv2.__version__)




