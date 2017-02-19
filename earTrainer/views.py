from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from earTrainer.forms import TrainerParams, CreateSamplesForm, TesterParams
from earTrainer.tasks import add, create_samples, start_training, start_testing
from earTrainer.models import SamplesModel,TrainerModel, TesterModel
from django.core import serializers

@login_required(login_url="../login/")
def home(request):
    all_samples = SamplesModel.objects.all().filter(status='FINISHED')

    all_trainings = TrainerModel.objects.all().filter(status='FINISHED')

    return render(request, "earTrainer.html",{'all_samples':all_samples,
                                              'all_trainings':all_trainings})


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
            pos_samples = form.clean_field('positive_samples')
            x_angle = form.clean_field('x_angle')
            y_angle = form.clean_field('y_angle')
            z_angle = form.clean_field('z_angle')
            max_dev = form.clean_field('max_dev')
            w = form.clean_field('w')
            h = form.clean_field('h')

            newSamples = SamplesModel(name=name,positives=pos_samples,x_angle=x_angle,
                                      y_angle=y_angle,z_angle=z_angle,max_dev=max_dev,w=w,h=h)
            newSamples.save()




            # start async sample create
            create_samples.delay(newSamples.pk)
    return render(request, 'earTrainer.html')


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

            newTrainer = TrainerModel(name=name,positives=positives, negatives=negative_samples,
                                      num_stages=num_stages,precalcValBuf=precalcValBuf,precalcIdxBuf=precalcIdxBuf,
                                      numThreads=numThreads, acceptanceBreak=acceptanceBreak, bt=bt,
                                      minHitRate=minHitRate, maxFalseAlarm=maxFalseAlarm, weightTrimRate=weightTrimRate,
                                      maxDepth=maxDepth, maxWeakCount=maxWeakCount, featureType=featureType)
            newTrainer.save()
            start_training.delay(newTrainer.pk)


    return render(request, 'earTrainer.html', {'form':form})

@login_required(login_url="../login/")
def start_testing_call(request):
    if request.method == 'POST':
        form = TesterParams(request.POST)
        if form.is_valid():
            training = TrainerModel.objects.get(pk=form.clean_field('xml_file'))
            print('Working with ',training)

            newTesting = TesterModel(trainer=training)
            newTesting.save()

            start_testing.delay(newTesting)
    return render(request, 'earTrainer.html')


@login_required(login_url="../login/")
def show_results(request):
    # collect all testing results
    all_results = TesterModel.objects.all()

    return render(request, 'results.html',{'results':all_results})









