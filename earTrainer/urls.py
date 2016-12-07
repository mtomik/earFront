from django.conf.urls import url, include

from . import views
from rest_framework import routers
from earTrainer.models import Job

router = routers.DefaultRouter()
router.register(r'jobs',views.JobViewSet)

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^test/$', views.test, name='test'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

]