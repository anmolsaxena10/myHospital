from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, Group
from .models import case
from datetime import datetime
from home.context_processors import hasGroup
from appointments.models import Appointment
# Create your views here.
#CREATE
@login_required
def generate(request):
    if hasGroup(request.user, 'receptionist'):
        c = {}
        c.update(csrf(request))
        c['patients'] = User.objects.filter(groups__name='patient')
        return render(request, 'case/generate.html', c)
    return HttpResponseRedirect('/home')

@login_required
def doGenerate(request):
    if hasGroup(request.user, 'receptionist'):
        patient = User.objects.get(username=request.POST.get('patient', ''))
        description = request.POST.get('description', '')
        filed_date = datetime.now()
        c = case(patient=patient, receptionist=request.user, description=description, filed_date=filed_date)
        c.save()
    return HttpResponseRedirect('/home')

#RETRIEVE
@login_required
def view(request):
    c = {}
    user = request.user
    if hasGroup(user, 'receptionist'):
        c['cases'] = case.objects.all()
    elif hasGroup(user, 'patient'):
        c['cases'] = case.objects.filter(patient=user)
    elif hasGroup(user, 'doctor'):
        c['cases'] = Appointment.objects.filter(doctor=user).case
    return render(request, 'case/view.html', c)

#UPDATE
@login_required
def change(request, id):
    pass

@login_required
def doChange(request):
    pass

#DELETE
@login_required
def delete(request, id):
    pass
