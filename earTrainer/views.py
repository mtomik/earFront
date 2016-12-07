from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from earTrainer.forms import TrainerParams
from earTrainer.main.createSamples import CreateSamples
from .serializers import JobSerializer
from .models import Job
from rest_framework import mixins, viewsets

class JobViewSet(mixins.CreateModelMixin,
                 mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    """
    API endpoint that allows jobs to be viewed or created.
    """
    queryset = Job.objects.all()
    serializer_class = JobSerializer

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
            a = CreateSamples("test", 10, 0.3, 0.3, 1.0, 40, 20, 40)
            a.start()


            return render(request, 'earTrainer.html')
    else:
        form = TrainerParams()

    return render(request, 'earTrainer.html', { 'form': form})




