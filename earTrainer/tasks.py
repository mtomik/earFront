from __future__ import absolute_import, unicode_literals
from celery import shared_task
from functools import wraps
from earDetectionWebApp.celery import app
from earTrainer.main.createSamples import CreateSamples
from earTrainer.main.trainer import Trainer
from earTrainer.tester.Tester import Tester

POSITIVES_COUNT = 1000

@shared_task
def add(x,y):
    return x+y

@app.task(bind = True)
def create_samples(self, sampleCount):

    global POSITIVES_COUNT
    POSITIVES_COUNT = sampleCount

    self.update_state(state="PROGRESS", meta={'progress': 10})
    sample_creator = CreateSamples("test", POSITIVES_COUNT, 0.3, 0.3, 1.0, 40, 20, 40)
    self.update_state(state="PROGRESS", meta={'progress': 20})
    sample_creator.start()

    return 'Samples: {0}'.format(sampleCount)

@app.task(bind = True)
def start_training(self):
    global POSITIVES_COUNT
    print('POS: ',POSITIVES_COUNT)

    # only 80% of positive samples
    positive_cut = int(POSITIVES_COUNT * 0.8)
    t = Trainer('test', positive_cut, 13000, 10, 1000, 3000, 4, 0.0001, 20, 40, 'RAB', 0.998, 0.35, 0.95, 1, 150, 'LBP')
    self.update_state(state="PROGRESS", meta={'progress': 10})
    t.start()

    return 'Finished!'


@app.task(bind = True)
def start_testing(self,name):
    print('Running tester for xml file ',name)
    test = Tester(xml_ear_file=name)
    result = test.start()

    return result






