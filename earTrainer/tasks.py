from __future__ import absolute_import, unicode_literals
from celery import shared_task
from functools import wraps
from earDetectionWebApp.celery import app
from earTrainer.main.createSamples import CreateSamples
from earTrainer.main.trainer import Trainer
from earTrainer.tester.Tester import Tester
from earTrainer.models import SamplesModel,TrainerModel, TesterModel, XmlModel

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
    return_code = sample_creator.start()

    self.update_state(state="PROGRESS", meta={'progress': 100})

    if return_code is 0:
        samples.status = "FINISHED"
    else:
        samples.status = "FAILED"

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
    return_code = t.start()
    self.update_state(state="PROGRESS", meta={'progress': 100})

    if return_code is 0:
        trainerModel.status = 'FINISHED'
    else:
        trainerModel.status = 'FAILED'

    trainerModel.save()

    return 'Finished!'


@app.task(bind = True)
def start_testing(self, testingModelPk):
    testingModel = TesterModel.objects.get(pk=testingModelPk)
    xml_path = testingModel.trainer.result_xml_path
    dir = testingModel.samples
    descriptor = testingModel.descriptor

    # copy from trainer result to test result dir

    print('Running tester for xml file ',xml_path)
    test = Tester(xml_ear_file=xml_path, trainer_name=testingModel.trainer.name, samples_dir=dir, descriptor_name=descriptor)
    try:
        result = test.start()
        testingModel.result = result
        testingModel.status = 'FINISHED'
    except FileNotFoundError as err:
        testingModel.result = -1
        testingModel.status = 'ERROR'
        testingModel.save()
        raise FileNotFoundError(err)

    testingModel.save()
    return result

@app.task(bind = True)
def start_testing_xml(self, testingModelPk,xml_pk):
    testingModel = TesterModel.objects.get(pk=testingModelPk)
    xml_path = XmlModel.objects.get(pk=xml_pk).xml_file.path

    # copy from trainer result to test result dir

    print('Running tester for xml file ',xml_path)
    test = Tester(xml_ear_file=xml_path,custom=True)
    result = test.start()

    testingModel.result = result
    testingModel.status = 'FINISHED'
    testingModel.save()
    return result









