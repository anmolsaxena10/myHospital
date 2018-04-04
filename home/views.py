from django.shortcuts import render,render_to_response
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required()
def home(request):
    return render(request, 'home/base.html')
