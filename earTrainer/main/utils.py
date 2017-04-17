from subprocess import Popen, PIPE
import os.path
import configparser
import numpy
import glob
from scipy import misc

from earDetectionWebApp.settings import BASE_DIR


class Utils:

    def __init__(self):
        self.x = 0

    @staticmethod
    def run_command(cmd, path=None):
        if path is not None:
            os.chdir(path)
        print('#Running command - ',cmd)

        p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
        out, err = p.communicate()
        print("Return code: ", p.returncode)
        print(out.rstrip(), err.rstrip())
        return p.returncode



class PropertyUtils:

    def __init__(self):
        self.config = configparser.RawConfigParser()
        self.config.read(os.path.join(BASE_DIR,'properties/main_config.properties'))

    def get_all(self,name):
        print(dict(self.config.items(name)))
        return dict(self.config.items(name))


class ImageUtils:

    def invert(self, dir):
        imgs = glob.glob(dir+'*.jpg')
        print('Flipping images..')
        for one in imgs:
            img = misc.imread(one)
            img = numpy.fliplr(img)
            misc.imsave(one,img)
        print('Done!')

