from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from .views import *

urlpatterns = [
    path('', view),
    url(r'generate/(?P<case_id>\d+)/', generate),
    path('do_generate/', doGenerate),
    url(r'delete/(?P<id>\d+)/', delete),
    path('pay/', pay),
    path('medicines/', viewMedicine)
]
