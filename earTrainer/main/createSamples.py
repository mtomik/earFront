from subprocess import Popen, PIPE

from earDetectionWebApp.settings import BASE_DIR
from earTrainer.main.utils import Utils, PropertyUtils
from earTrainer.models import SamplesModel
import os.path
from shutil import copyfile
from sys import platform
import shutil


class CreateSamples:

    def __init__(self, result_dir, sampleModel:SamplesModel):
        propUtil = PropertyUtils()

        # docker props
        if platform == 'linux':
            propsmain = propUtil.get_all('docker')
        else:
            propsmain = propUtil.get_all('main')

        propsenv = propUtil.get_all('env')


        self.workDir = propsmain.get('workdirpath')
        self.resultDir = os.path.join(self.workDir, result_dir)
        self.sampleCount = sampleModel.positives
        self.xAngle = sampleModel.x_angle
        self.yAngle = sampleModel.y_angle
        self.zAngle = sampleModel.z_angle
        self.iDev = sampleModel.max_dev
        self.w = sampleModel.w
        self.h = sampleModel.h
        self.positiveDat = self.workDir+'positives.dat'
        self.negativeDat = self.workDir+'negatives.dat'
        self.perlScript = os.path.join(BASE_DIR,'earTrainer/scripts/createtrainsamples.pl')
        self.samplesPath = propsmain.get('samplespath')
        self.os = propsenv.get('os')
        self.imageFormat = propsmain.get('imageformat')

        if not os.path.exists(self.workDir):
            os.mkdir(self.workDir)

        if not os.path.exists(self.resultDir):
            os.mkdir(self.resultDir)

    def start(self):
        if not os.path.exists(self.positiveDat):
            print('Creating positives.dat')
            self.create_dat(self, 'positives')

        if not os.path.exists(self.negativeDat):
            print('Creating negatives.dat')
            self.create_dat(self, 'negatives')


        # run positive sample creator
        self.create_pos_samples(self)

        # merge created positive samples to single VEC
        self.run_merge_vec()
        print('Creating samples done!')

    def test(self):
        cmd = 'ls -al'
        p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
        out, err = p.communicate()
        print("Return code: ", p.returncode)
        print(out.rstrip(), err.rstrip())

    @staticmethod
    def create_pos_samples(self,):
        print('Running create samples script!')
        shutil.rmtree(self.resultDir)
        opencv_sampler = 'opencv_createsamples.exe'

        if platform == 'linux':
            opencv_sampler = opencv_sampler[:-4]

        cmd = 'perl %s %s %s %s %i \"%s -bgcolor 0 -bgthresh 0 -maxxangle %.1f -maxyangle %.1f -maxzangle %.1f -maxidev %i -w %i -h %i \"' \
              % (self.perlScript, self.positiveDat, self.negativeDat,
                 self.resultDir, self.sampleCount, opencv_sampler, self.xAngle, self.yAngle, self.zAngle, self.iDev,
                 self.w, self.h)
        # creates samples on desired destination
        Utils.run_command(cmd)

    @staticmethod
    def create_dat(self, folder):
        datpath = self.workDir+folder+'.dat'

        if not os.path.exists(self.samplesPath+folder):
            print('This path: ', self.samplesPath+folder, ' doesnt exists!')
            return

        if os.path.exists(datpath):
            os.remove(datpath)

        count = 0
        f = open(datpath, 'w+')

        for oneJpg in os.listdir(self.samplesPath+folder):
            if oneJpg.endswith('.'+self.imageFormat):
                f.write(os.path.join(self.samplesPath, folder, oneJpg)+'\n')
                count += 1

        print('Images found in ', folder, ': ', count)
        f.close()

    def run_merge_vec(self):
        if not os.path.exists(os.path.join(self.workDir, 'mergevec.py')):
            copyfile('../scripts/mergevec.py', self.workDir+'mergevec.py')

        Utils.run_command('python mergevec.py -v '+self.resultDir+' -o '+self.resultDir+'/merged.vec', self.workDir)
        #os.chdir('../scripts')
        #os.system('mergevec.py -v '+self.resultDir+' -o merged.vec')



