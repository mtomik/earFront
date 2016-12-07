from subprocess import Popen, PIPE

from earDetectionWebApp.settings import BASE_DIR
from earTrainer.main.utils import Utils, PropertyUtils
import os.path
from shutil import copyfile


class CreateSamples:

    def __init__(self, result_dir, sample_count, x_angle, y_angle, z_angle, i_dev, w, h):
        propUtil = PropertyUtils()
        propsmain = propUtil.get_all('main')
        propsenv = propUtil.get_all('env')


        self.workDir = propsmain.get('workdirpath')
        self.resultDir = os.path.join(self.workDir, result_dir)
        self.sampleCount = sample_count
        self.xAngle = x_angle
        self.yAngle = y_angle
        self.zAngle = z_angle
        self.iDev = i_dev
        self.w = w
        self.h = h
        self.positiveDat = self.workDir+'positives.dat'
        self.negativeDat = self.workDir+'negatives.dat'
        self.perlScript = os.path.join(BASE_DIR,'earTrainer/scripts/createtrainsamples.pl')
        self.samplesPath = propsmain.get('samplespath')
        self.os = propsenv.get('os')
        self.imageFormat = propsmain.get('imageformat')

        if not os.path.exists(self.workDir):
            os.mkdir(self.workDir)

    def start(self):
        if not os.path.exists(self.positiveDat):
            print('Creating positives.dat')
            self.create_dat(self, 'positives')

        if not os.path.exists(self.negativeDat):
            print('Creating negatives.dat')
            self.create_dat(self, 'negatives')

        print('Running create samples script!')
        cmd = 'perl %s %s %s %s %i \"opencv_createsamples.exe -bgcolor 0 -bgthresh 0 -maxxangle %.1f -maxyangle %.1f -maxzangle %.1f -maxidev %i -w %i -h %i \"' \
              % (self.perlScript, self.positiveDat,self.negativeDat,
                 self.resultDir, self.sampleCount, self.xAngle, self.yAngle, self.zAngle, self.iDev, self.w, self.h)
        # creates samples on desired destination
        Utils.run_command(cmd)

        # merge created positive samples to single VEC
        self.run_merge_vec()

    def test(self):
        cmd = 'ls -al'
        p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
        out, err = p.communicate()
        print("Return code: ", p.returncode)
        print(out.rstrip(), err.rstrip())

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

        Utils.run_command('python mergevec.py -v '+self.resultDir+' -o merged.vec', self.workDir)
        #os.chdir('../scripts')
        #os.system('mergevec.py -v '+self.resultDir+' -o merged.vec')



