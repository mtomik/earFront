import configparser
from subprocess import Popen, PIPE
from earTrainer.main.utils import Utils, PropertyUtils
from decimal import *
import os
from sys import platform
from earDetectionWebApp.settings import BASE_DIR
from glob import glob


class Trainer:

    def __init__(self, resultDir, numPos, numNeg, numStages,
                 precalcValBuf, precalcIdxBuf, numThreads, acceptanceBreak,
                 w, h, bt, minHitRate, maxFalseAlarm, weightTrimRate, maxDepth, maxWeakCount, featureType ):

        properties = PropertyUtils()

        # docker props
        if platform == 'linux':
            propsmain = properties.get_all('docker')
        else:
            propsmain = properties.get_all('main')


        self.resultDir = resultDir

        #ukladanie do vedlajsieho precinka
        self.resultDir = propsmain.get('resultsdir')
        self.workDir = propsmain.get('workdirpath')

        self.numPos = numPos
        self.numNeg = numNeg
        self.numStages = numStages
        self.precalcValBuf = precalcValBuf
        self.precalcIdxBuf = precalcIdxBuf
        self.numThreads = numThreads
        self.acceptBreak = acceptanceBreak
        self.w = w
        self.h = h
        self.bt = bt
        self.minHitRate = minHitRate
        self.maxFalseAlarm = maxFalseAlarm
        self.weightTrimRate = weightTrimRate
        self.maxDepth = maxDepth
        self.maxWeakCount = maxWeakCount
        self.featureType = featureType


    def start(self):
        print('Running training')

        last = glob(self.resultDir+'/*/')

        #ak je prazdny.. vytvor odznova
        if len(last) == 0:
            lastIndex = 1
        else:
            # sprav novy dir ako posledny index o jedna viac
            lastIndex = int(os.path.basename(os.path.dirname(last[-1]))) + 1

        self.resultDir = os.path.join(os.path.dirname(self.resultDir), str(lastIndex))
        if not os.path.exists(self.resultDir):
            os.mkdir(self.resultDir)


        opencv_trainer = 'opencv_traincascade.exe'

        if platform == 'linux':
            opencv_trainer = opencv_trainer[:-4]

        cmd = '%s -data %s -vec merged.vec -bg negatives.dat -numPos %i -numNeg %i -numStages %i -precalcValBufSize %i -precalcIdxBufSize %i' \
              ' -numThreads %i -acceptanceRatioBreakValue %.4f -w %i -h %i -bt %s -minHitRate %.3f -maxFalseAlarmRate %.3f -weightTrimRate %.2f -maxDepth %i -maxWeakCount %i -featureType %s' \
            % (opencv_trainer, self.resultDir, self.numPos, self.numNeg, self.numStages, self.precalcValBuf, self.precalcIdxBuf,
            self.numThreads, self.acceptBreak, self.w, self.h, self.bt, self.minHitRate, self.maxFalseAlarm, self.weightTrimRate, self.maxDepth, self.maxWeakCount, self.featureType)

        Utils.run_command(cmd, self.workDir)
        # premenuj podla verzie
        os.rename(os.path.join(self.resultDir,'cascade.xml'),os.path.join(self.resultDir,str(lastIndex)+'.xml'))
