from django.urls import path, include
from django.conf.urls import url
from .views import *

urlpatterns = [
    path('', view),
    path('generate/', generate),
    path('do_generate/', doGenerate),
    url(r'change/(?P<id>\d+)/', change),
    path('do_change/', doChange),
    url(r'delete/(?P<id>\d+)/', delete),
]
