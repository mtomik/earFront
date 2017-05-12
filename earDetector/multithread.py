import threading
import queue
from earDetector.earDetect import earDetect,earDetectParams
import time



class thread_detector(threading.Thread):

    def __init__(self, type,xml_file,q,params):
        threading.Thread.__init__(self,daemon=True)
        self.type = type
        self.q = q
        self.detect = earDetect(xml_file, type)
        self.params = params


    def run(self):
        print('in')
        result = self.detect.detect_from_bytes(self.params)
        self.q.put((self.type,result))

def create_async_multi_detect(left_xml,right_xml,params:earDetectParams):
    q = queue.Queue()

    if left_xml:
        left = thread_detector('lave',left_xml,q,params)
        left.start()

    if right_xml:
        right = thread_detector('prave',right_xml,q,params)
        right.start()

    # get first one
    result = q.get()

    # if no result (images_url) -> check another detector
    if not result[1][0]:
        result = q.get()

    return result
