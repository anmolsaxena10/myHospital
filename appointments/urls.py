from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from .views import *

urlpatterns = [
    path('', view),
    path('book/', book),
    path('do_book/', doBook),
    url(r'change_appointment/(?P<id>\d+)/', changeAppointment),
    path('do_change/', doChange),
    url(r'delete/(?P<id>\d+)/', delete),
]
