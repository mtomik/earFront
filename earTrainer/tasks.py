from __future__ import absolute_import, unicode_literals
from celery import shared_task
from functools import wraps
from earDetectionWebApp.celery import app
from earTrainer.main.createSamples import CreateSamples
from earTrainer.main.trainer import Trainer
from earTrainer.tester.Tester import Tester

from earTrainer.models import SamplesModel,TrainerModel, TesterModel

@shared_task
def add(x,y):
    return x+y

@app.task(bind = True)
def create_samples(self,samplesId):

    # global POSITIVES_COUNT
    # POSITIVES_COUNT = samples.pos_samples
    samples = SamplesModel.objects.get(pk=samplesId)
    assert samples is not None

    print('in async: ',samples)

    self.update_state(state="PROGRESS", meta={'progress': 10})
    sample_creator = CreateSamples(samples.name,samples)
    self.update_state(state="PROGRESS", meta={'progress': 20})
    sample_creator.start()

    self.update_state(state="PROGRESS", meta={'progress': 100})

    samples.status = "FINISHED"
    samples.save()

    return 'Samples: {0}'.format(samples.positives)

@app.task(bind = True)
def start_training(self, trainerId):
    trainerModel = TrainerModel.objects.get(pk=trainerId)
    positives = trainerModel.positives.positives
    print('POS: ',positives)

    # only 80% of positive samples
    positive_cut = int(positives * 0.8)
    trainerModel.positives.positives = positive_cut
    trainerModel.save()

    t = Trainer(trainerModel)
    self.update_state(state="PROGRESS", meta={'progress': 10})
    t.start()
    self.update_state(state="PROGRESS", meta={'progress': 100})

    trainerModel.status = 'FINISHED'
    trainerModel.save()

    return 'Finished!'


@app.task(bind = True)
def start_testing(self,tesingModel:TesterModel):
    name = tesingModel.trainer.name

    print('Running tester for xml file ',name)
    test = Tester(xml_ear_file=name)
    result = test.start()

    tesingModel.result = result
    tesingModel.status = 'FINISHED'
    tesingModel.save()

    return result






