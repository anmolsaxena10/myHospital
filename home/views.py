from django.shortcuts import render,render_to_response
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
@login_required()
def home(request):
    messages.add_message(request, messages.INFO, 'Welcome to The Hospital Portal.')
    return render(request, 'home/base.html')
