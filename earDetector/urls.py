from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^detect/$', views.detect, name='detect'),
    url(r'^detectSciKit/$',views.detectSciKit, name='detectSciKit'),
]