from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.template.context_processors import csrf

# Create your views here.
def login(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect('/home')
	else:
		c = {}
		c.update(csrf(request))
		return render(request, 'loginmodule/login.html', c)

def auth_view(request):
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')
	user = auth.authenticate(username=username, password=password)

	if user is not None:
		auth.login(request, user)
		return HttpResponseRedirect('/home')
	else:
		return HttpResponseRedirect('/login')

def logout(request):
	if request.user.is_authenticated:
		auth.logout(request)
	return HttpResponseRedirect('/login')
