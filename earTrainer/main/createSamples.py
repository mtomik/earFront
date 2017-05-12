from subprocess import Popen, PIPE
from earTrainer.main.utils import Utils
from earTrainer.models import SamplesModel
import os.path
from shutil import copyfile
from sys import platform
import shutil
from earDetectionWebApp.settings import BASE_DIR, properties as propsmain

class CreateSamples:

    def __init__(self, result_dir, sampleModel:SamplesModel):

        self.workDir = propsmain.get('workdirpath')
        self.resultDir = os.path.join(self.workDir, result_dir)
        self.sampleCount = sampleModel.positives
        self.xAngle = sampleModel.x_angle
        self.yAngle = sampleModel.y_angle
        self.zAngle = sampleModel.z_angle
        self.iDev = sampleModel.max_dev
        self.w = sampleModel.w
        self.h = sampleModel.h

        self.perlScript = os.path.join(BASE_DIR,'earTrainer/scripts/createtrainsamples.pl')
        self.samplesRootPath = propsmain.get('samplespath')
        self.samplesDir = sampleModel.samples_dir
        self.negativesDir = 'negatives'

        self.imageFormat = propsmain.get('imageformat')
        self.samplesModel = sampleModel

        self.positivesDat = 'None'
        self.negativesDat = 'None'

        if not os.path.exists(self.workDir):
            os.mkdir(self.workDir)
        if os.path.exists(self.resultDir):
            shutil.rmtree(self.resultDir)
        os.mkdir(self.resultDir)

    def start(self):

        # Vytvorenie deskriptora ( zoznam cies ku vsetkym snimkom )
        self.positivesDat = self.create_positive_dat()
        self.negativesDat = self.create_negative_dat()

        # ulozenie stavu procesu do DB
        self.samplesModel.status = 'RUNNING'
        self.samplesModel.save()

        # vytvorenie pozitivnych VEC suborov
        self.create_pos_samples()

        # Spojenie vsetkych VEC do jedneho
        return self.run_merge_vec()

    def test(self):
        cmd = 'ls -al'
        p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
        out, err = p.communicate()
        print("Return code: ", p.returncode)
        print(out.rstrip(), err.rstrip())

    def create_pos_samples(self,):
        print('Running create samples script!')
        opencv_sampler = 'opencv_createsamples.exe'

        if platform == 'linux':
            opencv_sampler = opencv_sampler[:-4]

        cmd = 'perl %s %s %s %s %i \"%s -bgcolor 0 -bgthresh 0 -maxxangle %.1f -maxyangle %.1f -maxzangle %.1f -maxidev %i -w %i -h %i \"' \
              % (self.perlScript, self.positivesDat, self.negativesDat,
                 self.resultDir, self.sampleCount, opencv_sampler, self.xAngle, self.yAngle, self.zAngle, self.iDev,
                 self.w, self.h)
        # creates samples on desired destination
        Utils.run_command(cmd)

    def create_positive_dat(self):
        return self.create_dat(self.samplesDir)

    def create_negative_dat(self):
        return self.create_dat(self.negativesDir,True)

    def create_dat(self, source_folder, isnegative=False):
        images_path = os.path.join(self.samplesRootPath,source_folder)
        print('ImagesPath '+images_path)
        if isnegative:
            result_dat_path = os.path.join(self.workDir,'negatives.dat')
        else:
            result_dat_path = os.path.join(self.resultDir,'positive.dat')

        if not os.path.exists(images_path):
            print('Source folder: ', images_path, ' doesn\'t exists!')
            return

        count = 0
        with open(result_dat_path,'w+') as f:
            for oneJpg in os.listdir(images_path):
                if oneJpg.endswith('.'+self.imageFormat):
                    f.write(os.path.join(images_path, oneJpg)+'\n')
                    count += 1

        print(' Images found in ', source_folder, ': ', count,' of type: '+self.imageFormat)
        return result_dat_path

    def run_merge_vec(self):
        if not os.path.exists(os.path.join(self.workDir, 'mergevec.py')):
            copyfile(BASE_DIR+'/earTrainer/scripts/mergevec.py', self.workDir+'mergevec.py')

        return_code = Utils.run_command('python3 mergevec.py -v '+self.resultDir+' -o '+self.resultDir+'/merged.vec', self.workDir)
        #os.chdir('../scripts')
        #os.system('mergevec.py -v '+self.resultDir+' -o merged.vec')

        return return_code



