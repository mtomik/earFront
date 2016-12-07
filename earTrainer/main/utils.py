from subprocess import Popen, PIPE
import os.path
import configparser

from earDetectionWebApp.settings import BASE_DIR


class Utils:

    def __init__(self):
        self.x = 0

    @staticmethod
    def run_command(cmd, path=None):
        if path is not None:
            os.chdir(path)

        p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
        out, err = p.communicate()
        print("Return code: ", p.returncode)
        print(out.rstrip(), err.rstrip())
        return out, err


class PropertyUtils:

    def __init__(self):
        self.config = configparser.RawConfigParser()
        self.config.read(os.path.join(BASE_DIR,'properties/main_config.properties'))
        print(self.config.get('main','workDirPath'))

    def get_all(self,name):
        print(dict(self.config.items(name)))
        return dict(self.config.items(name))