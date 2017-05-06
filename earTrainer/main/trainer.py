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

        self.opencv_trainer = 'opencv_traincascade.exe'
        if platform == 'linux':
            self.opencv_trainer = self.opencv_trainer[:-4]


    def start(self):
        if self.trainerModel.status is 'RUNNING':
            return self.re_run()

        return self.full_run()

    def full_run(self):
        print('Running full training')
        lastIndex = 0
        while os.path.exists(os.path.join(self.resultDir, str(lastIndex))):
            lastIndex += 1

        self.resultDir = os.path.join(os.path.dirname(self.resultDir), str(lastIndex))
        if not os.path.exists(self.resultDir):
            os.mkdir(self.resultDir)

        merged_file = os.path.join(self.samplesDir, 'merged.vec')

        cmd = '%s -data %s -vec %s -bg negatives.dat -numPos %i -numNeg %i -numStages %i -precalcValBufSize %i -precalcIdxBufSize %i' \
              ' -numThreads %i -acceptanceRatioBreakValue %.8f -w %i -h %i -bt %s -minHitRate %.4f -maxFalseAlarmRate %.4f -weightTrimRate %.2f -maxDepth %i -maxWeakCount %i -featureType %s -mode %s' \
              % (self.opencv_trainer, self.resultDir, merged_file, self.numPos, self.numNeg, self.numStages,
                 self.precalcValBuf, self.precalcIdxBuf,
                 self.numThreads, self.acceptBreak, self.w, self.h, self.bt, self.minHitRate, self.maxFalseAlarm,
                 self.weightTrimRate, self.maxDepth, self.maxWeakCount, self.featureType, self.mode)

        self.trainerModel.full_cmd = cmd
        self.trainerModel.status = 'RUNNING'
        self.trainerModel.save()

        return_code = Utils.run_command(cmd, self.workDir)

        if return_code is 0:
            self.trainerModel.result_xml_path = os.path.join(self.resultDir, 'cascade.xml')
            self.trainerModel.save()

        return return_code

    def re_run(self):
        return_code = Utils.run_command(self.trainerModel.full_cmd, self.workDir)

        if return_code is 0:
            self.trainerModel.result_xml_path = os.path.join(self.resultDir, 'cascade.xml')
            self.trainerModel.save()

        return return_code


