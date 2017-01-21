from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from earTrainer.forms import TrainerParams, CreateSamplesForm
from earTrainer.tasks import add, create_samples, start_training, start_testing

@login_required(login_url="../login/")
def home(request):
    return render(request, "earTrainer.html")


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
def test(request):
    if request.method == 'POST':
        print('is post')
        form = TrainerParams(request.POST)
        print(form)
        if form.is_valid():
            print (request.POST.get('first_param'))
            # a = CreateSamples("test", 10, 0.3, 0.3, 1.0, 40, 20, 40)
            # a.start()
            print(add.delay(10, 5))


            return render(request, 'earTrainer.html')
    else:
        form = TrainerParams()

    return render(request, 'earTrainer.html', { 'form': form})

@login_required(login_url="../login/")
def create_sample_call(request):
    if request.method == 'POST':
        form = CreateSamplesForm(request.POST)
        if form.is_valid():
            pos_samples = int(request.POST.get('positive_samples'))
            # spusti vytvaranie samplov
            create_samples.delay(pos_samples)
    return render(request, 'earTrainer.html')


@login_required(login_url="../login/")
def start_training_call(request):
    if request.method == 'POST':
        start_training.delay()
    return render(request, 'earTrainer.html')

@login_required(login_url="../login/")
def start_testing_call(request):
    if request.method == 'POST':
        xml_file = request.POST.get('xml_file')
        start_testing.delay(xml_file)
    return render(request, 'earTrainer.html')









