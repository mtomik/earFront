import ConfigParser
from subprocess import Popen, PIPE
from utils import Utils
from decimal import *
import os


class Trainer:

    def __init__(self, resultDir, numPos, numNeg, numStages,
                 precalcValBuf, precalcIdxBuf, numThreads, acceptanceBreak,
                 w, h, bt, minHitRate, maxFalseAlarm, weightTrimRate, maxDepth, maxWeakCount, featureType ):
        parser = ConfigParser.RawConfigParser()
        parser.read('../properties/main_config.properties')

        self.resultDir = resultDir
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

        if not os.path.exists('../scripts/'+self.resultDir):
            os.makedirs('../scripts/'+self.resultDir)



    def start(self):
        print('Running training')
        cmd = 'opencv_traincascade.exe -data %s -vec merged.vec -bg negatives.dat -numPos %i -numNeg %i -numStages %i -precalcValBufSize %i -precalcIdxBufSize %i' \
              ' -numThreads %i -acceptanceRatioBreakValue %.4f -w %i -h %i -bt %s -minHitRate %.3f -maxFalseAlarmRate %.3f -weightTrimRate %.2f -maxDepth %i -maxWeakCount %i -featureType %s' \
            % (str(self.resultDir,'utf-8'), self.numPos, self.numNeg, self.numStages, self.precalcValBuf, self.precalcIdxBuf,
            self.numThreads, self.acceptBreak, self.w, self.h, self.bt, self.minHitRate, self.maxFalseAlarm, self.weightTrimRate, self.maxDepth, self.maxWeakCount, self.featureType)

        print(cmd)
        Utils.run_command(cmd, '../scripts')
        # TODO: Create training runner