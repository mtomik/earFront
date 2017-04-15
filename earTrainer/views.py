from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from earTrainer.forms import TrainerParams, CreateSamplesForm, TesterParams, XmlUploadForm
from earTrainer.tasks import add, create_samples, start_training, start_testing, start_testing_xml
from earTrainer.models import SamplesModel,TrainerModel, TesterModel, XmlModel
from django.contrib import messages
import glob
import os
from earDetectionWebApp.settings import properties
from earTrainer.tester.Tester import Tester

@login_required(login_url="../login/")
def home(request):
    return render(request, "earTrainer.html",{'all_samples':get_all_samples(),
                                              'all_trainings':get_all_trainings(),
                                              'all_samples_dirs':get_all_samples_dir(),
                                              'all_test_samples':get_all_test_dir()})

@login_required
def start(request):
    # username = request.POST['username']
    # password = request.POST['password']
    # user = authenticate(username=username, password=password)
    # if user is not None:
    #     login(request, user)
    #     print 'User authenticated'
    # else:
    #     print 'failed to authenticate'
    if request.user.is_authenticated:
        return HttpResponse('hello authenticated')
    else:
        return HttpResponse('not authenticated')


@login_required(login_url="../login/")
def create_sample_call(request):
    if request.method == 'POST':
        form = CreateSamplesForm(request.POST)
        if form.is_valid():

            name = form.clean_field('name')
            samples_dir = form.clean_field('samples_dir')
            pos_samples = form.clean_field('positive_samples')
            x_angle = form.clean_field('x_angle')
            y_angle = form.clean_field('y_angle')
            z_angle = form.clean_field('z_angle')
            max_dev = form.clean_field('max_dev')
            w = form.clean_field('w')
            h = form.clean_field('h')

            newSamples = SamplesModel(name=name,samples_dir=samples_dir, positives=pos_samples,x_angle=x_angle,
                                      y_angle=y_angle,z_angle=z_angle,max_dev=max_dev,w=w,h=h)
            newSamples.save()




            # start async sample create
            create_samples.delay(newSamples.pk)

            messages.success(request, "Pozitivne vzorky sa zacali vytvarat..")


    return render(request, 'earTrainer.html',{'all_samples':get_all_samples(),
                                              'all_trainings':get_all_trainings(),
                                              'all_samples_dirs': get_all_samples_dir(),
                                              'all_test_samples':get_all_test_dir()})

@login_required(login_url="../login/")
def start_training_call(request):
    form = None
    if request.method == 'POST':
        form = TrainerParams(request.POST)

        if form.is_valid():
            name = form.clean_field('name')
            positives = SamplesModel.objects.get(pk=form.clean_field('samplesId'))
            negative_samples = form.clean_field('negative_samples')
            num_stages = form.clean_field('num_stages')
            precalcValBuf = form.clean_field('precalcValBuf')
            precalcIdxBuf = form.clean_field('precalcIdxBuf')
            numThreads = form.clean_field('numThreads')
            acceptanceBreak = form.clean_field('acceptanceBreak')
            bt = form.clean_field('bt')
            minHitRate = form.clean_field('minHitRate')
            maxFalseAlarm = form.clean_field('maxFalseAlarm')
            weightTrimRate = form.clean_field('weightTrimRate')
            maxDepth = form.clean_field('maxDepth')
            maxWeakCount = form.clean_field('maxWeakCount')
            featureType = form.clean_field('featureType')
            mode = form.clean_field('mode')

            newTrainer = TrainerModel(name=name,positives=positives, negatives=negative_samples,
                                      num_stages=num_stages,precalcValBuf=precalcValBuf,precalcIdxBuf=precalcIdxBuf,
                                      numThreads=numThreads, acceptanceBreak=acceptanceBreak, bt=bt,
                                      minHitRate=minHitRate, maxFalseAlarm=maxFalseAlarm, weightTrimRate=weightTrimRate,
                                      maxDepth=maxDepth, maxWeakCount=maxWeakCount, featureType=featureType,mode=mode)
            newTrainer.save()
            start_training.delay(newTrainer.pk)

            messages.success(request, "Trenovanie klasifikatora prave zacalo.")

    return render(request, 'earTrainer.html', {'form':form,'all_samples':get_all_samples(),
                                              'all_trainings':get_all_trainings(),
                                               'all_samples_dirs': get_all_samples_dir(),
                                               'all_test_samples': get_all_test_dir()})


@login_required(login_url="../login/")
def start_testing_call(request):
    form = None
    if request.method == 'POST':
        form = TesterParams(request.POST)
        if form.is_valid():
            training = TrainerModel.objects.get(pk=form.clean_field('xml_file'))
            samples_dir = form.clean_field('test_samples_dir')

            newTesting = TesterModel(trainer=training,samples=samples_dir)
            newTesting.save()

            try:
                start_testing.delay(newTesting.pk)
                messages.success(request, "Testovanie klasifikatora zacalo.")
            except FileNotFoundError as err:
                messages.warning(request,err,fail_silently=True)


    return render(request, 'earTrainer.html', {'form':form, 'all_samples':get_all_samples(),
                                              'all_trainings':get_all_trainings(),
                                               'all_samples_dirs': get_all_samples_dir(),
                                               'all_test_samples': get_all_test_dir()})


@login_required(login_url="../login/")
def start_testing_custom(request):
    if request.method == 'POST':
        form = XmlUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save()
            samples_dir = form.clean_field('test_samples_dir')

            name = request.FILES['xml_file'].name
            newTesting = TesterModel(name=name,samples=samples_dir)

            try:
                test = Tester(xml_ear_file=file.xml_file.path, custom=True, samples_dir=samples_dir)
                result = test.start()
                newTesting.result = result
                newTesting.status = 'FINISHED'
                messages.success(request, "Testovanie klasifikatora zacalo.")
            except FileNotFoundError as err:
                newTesting.result = -1
                newTesting.status = 'ERROR'
                messages.warning(request,err,fail_silently=True)

            newTesting.save()

    else:
        form = XmlUploadForm()

    return render(request, 'earTrainer.html', {'form': form, 'all_samples': get_all_samples(),
                                               'all_trainings': get_all_trainings(),
                                               'all_samples_dirs': get_all_samples_dir(),
                                               'all_test_samples': get_all_test_dir()})


@login_required(login_url="../login/")
def show_results(request):
    # collect all testing results
    all_results = TesterModel.objects.all()
    all_trainers = TrainerModel.objects.all()
    all_samples = SamplesModel.objects.all()

    return render(request, 'results.html',{'all_results':all_results,
                                           'all_trainers':all_trainers,
                                           'all_samples':all_samples})


def get_all_samples():
    return SamplesModel.objects.all().filter(status='FINISHED')


def get_all_trainings():
    return TrainerModel.objects.all().filter(status='FINISHED')

def get_all_samples_dir():
    return get_dirs(properties.get('samplespath'))

def get_all_test_dir():
    return get_dirs(properties.get('testerdir'),['xmls','results'])


def get_dirs(dir_path,exclude=None):
    all_dirs = glob.glob(dir_path + "*")
    dirs = list()
    for one in all_dirs:
        if os.path.isdir(one):
            if exclude:
                if os.path.basename(one) in exclude:
                    continue

            dirs.append(os.path.basename(one))
    return dirs









