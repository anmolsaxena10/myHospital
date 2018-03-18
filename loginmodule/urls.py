from django.urls import path
from loginmodule.views import auth_view
from django.contrib.auth import views as auth_views
from django.conf.urls import url

urlpatterns = [
	path('auth', auth_view),
]
