from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, Group
from .models import Report
from datetime import datetime
from home.context_processors import hasGroup
from appointments.models import Appointment
from case.models import case
from django.contrib import messages

# Create your views here.

#CREATE
@login_required
def generate(request):
    if hasGroup(request.user, 'lab_attendant'):
        c = {}
        c.update(csrf(request))
        c['cases'] = case.objects.all()
        return render(request, 'report/generate.html', c)
    messages.add_message(request, messages.WARNING, 'Access Denied.')
    return HttpResponseRedirect('/home')

@login_required
def doGenerate(request):
    if hasGroup(request.user, 'lab_attendant'):
        c = case.objects.get(id=request.POST.get('case'))
        description = request.POST.get('description', '')
        generated_date = datetime.now()
        report = Report(case=c, lab_attendant=request.user, description=description, generated_date=generated_date)
        report.save()
        messages.add_message(request, messages.INFO, 'Report Successfully Generated.')
        return HttpResponseRedirect('/reports')
    messages.add_message(request, messages.WARNING, 'Access Denied.')
    return HttpResponseRedirect('/home')

#RETRIEVE
@login_required
def view(request):
    c = {}
    user = request.user
    if hasGroup(user, 'lab_attendant'):
        c['isLabAttendant'] = True
        c['reports'] = Report.objects.filter(lab_attendant=request.user)
    elif hasGroup(user, 'patient'):
        c['reports'] = [report for report in Report.objects.all() if report.case.patient==request.user]
    else:
        messages.add_message(request, messages.WARNING, 'Access Denied.')
        return HttpResponseRedirect('/home')
    return render(request, 'report/view.html', c)

#UPDATE
@login_required
def change(request, id):
    '''user = request.user
    if hasGroup(user, 'lab_attendant'):

        return render(request, 'report/change.html', c)
    messages.add_message(request, messages.WARNING, 'Access Denied.')'''
    return HttpResponseRedirect('/home')

@login_required
def doChange(request):
    pass

#DELETE
@login_required
def delete(request, id):
    user = request.user
    if hasGroup(user, 'lab_attendant'):
        Report.objects.get(id=id).delete()
    return HttpResponseRedirect('/home')
