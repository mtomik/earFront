from earTrainer.main.utils import Utils
import os
from sys import platform
from earDetectionWebApp.settings import BASE_DIR,properties as propsmain
from glob import glob
from earTrainer.models import TrainerModel

class Trainer:

    def __init__(self, trainModel:TrainerModel ):



        self.resultDir = trainModel.name

        #ukladanie do vedlajsieho precinka
        self.resultDir = propsmain.get('resultsdir')
        self.workDir = propsmain.get('workdirpath')
        self.samplesDir = trainModel.positives.name

        self.numPos = trainModel.positives.positives
        self.numNeg = trainModel.negatives
        self.numStages = trainModel.num_stages
        self.precalcValBuf = trainModel.precalcValBuf
        self.precalcIdxBuf = trainModel.precalcIdxBuf
        self.numThreads = trainModel.numThreads
        self.acceptBreak = trainModel.acceptanceBreak
        self.w = trainModel.positives.w
        self.h = trainModel.positives.h
        self.bt = trainModel.bt
        self.minHitRate = trainModel.minHitRate
        self.maxFalseAlarm = trainModel.maxFalseAlarm
        self.weightTrimRate = trainModel.weightTrimRate
        self.maxDepth = trainModel.maxDepth
        self.maxWeakCount = trainModel.maxWeakCount
        self.featureType = trainModel.featureType
        self.trainerModel = trainModel
        self.mode = trainModel.mode


    def start(self):
        print('Running training')

        last = glob(self.resultDir+'/*/')

        #ak je prazdny.. vytvor odznova
        if len(last) == 0:
            lastIndex = 1
        else:
            # sprav novy dir ako posledny index o jedna viac
            lastIndex = int(os.path.basename(os.path.dirname(last[-1]))) + 1

        lastIndex = 0
        while os.path.exists(os.path.join(self.resultDir,str(lastIndex))):
            lastIndex += 1


        self.resultDir = os.path.join(os.path.dirname(self.resultDir), str(lastIndex))
        if not os.path.exists(self.resultDir):
            os.mkdir(self.resultDir)


        opencv_trainer = 'opencv_traincascade.exe'

        if platform == 'linux':
            opencv_trainer = opencv_trainer[:-4]

        merged_file = os.path.join(self.samplesDir,'merged.vec')



        cmd = '%s -data %s -vec %s -bg negatives.dat -numPos %i -numNeg %i -numStages %i -precalcValBufSize %i -precalcIdxBufSize %i' \
              ' -numThreads %i -acceptanceRatioBreakValue %.8f -w %i -h %i -bt %s -minHitRate %.3f -maxFalseAlarmRate %.4f -weightTrimRate %.2f -maxDepth %i -maxWeakCount %i -featureType %s -mode %s' \
            % (opencv_trainer, self.resultDir, merged_file, self.numPos, self.numNeg, self.numStages, self.precalcValBuf, self.precalcIdxBuf,
            self.numThreads, self.acceptBreak, self.w, self.h, self.bt, self.minHitRate, self.maxFalseAlarm, self.weightTrimRate, self.maxDepth, self.maxWeakCount, self.featureType, self.mode)

        self.trainerModel.status = 'RUNNING'
        self.trainerModel.save()

        return_code = Utils.run_command(cmd, self.workDir)

        self.trainerModel.result_xml_path=os.path.join(self.resultDir,'cascade.xml')
        self.trainerModel.save()
        # premenuj podla verzie
        #os.rename(os.path.join(self.resultDir,'cascade.xml'),os.path.join(self.resultDir,str(lastIndex)+'.xml'))

        return return_code
