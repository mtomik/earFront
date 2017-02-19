from django.conf.urls import url, include

from . import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^create_samples/$', views.create_sample_call, name='samples'),
    url(r'^trainer/$', views.start_training_call, name='trainer'),
    url(r'^tester/$', views.start_testing_call, name='tester'),
    url(r'^results/$',views.show_results, name='results')

]