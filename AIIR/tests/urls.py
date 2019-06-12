from django.conf.urls import url, include
from .import views
from django.views.decorators.csrf import csrf_exempt
import json

urlpatterns = [
    url(r'^run$', views.nowa, name='nowa'),
    url(r'^$', csrf_exempt(views.index), name='index'),
    url(r'^create$', csrf_exempt(views.create_new_task), name='create'),
    url(r'^nodeInfo$', csrf_exempt(views.nodeInfo), name='node info'),
    url(r'^(?P<login>[\w]+)/input/(?P<taskId>[0-9]+)$', csrf_exempt(views.input_data), name='input_data'),
    url(r'^(?P<login>[\w]+)/output/(?P<taskId>[0-9]+)$', csrf_exempt(views.output_data), name='output_data'),
    url(r'^(?P<login>[\w]+)/tasks', csrf_exempt(views.tasks), name='tasks'),
]
