from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, Group
from .models import Appointment
from datetime import datetime
from home.context_processors import hasGroup
from case.models import case
# Create your views here.

#CREATE
@login_required
def book(request):
    user = request.user
    if hasGroup(user, 'receptionist'):
        c = {}
        c.update(csrf(request))
        c['patients'] = User.objects.filter(groups__name='patient')
        c['doctors'] = User.objects.filter(groups__name='doctor')
        c['cases'] = case.objects.all()
        return render(request, 'appointments/book_appointment.html', c)
    return HttpResponseRedirect('/home')

@login_required
def doBook(request):
    user = request.user
    if hasGroup(user, 'receptionist'):
        patient = User.objects.get(username=request.POST.get('patient', ''))
        doctor = User.objects.get(username=request.POST.get('doctor', ''))
        c = case.objects.get(pk=int(request.POST.get('case', '')))
        appointment_time = request.POST.get('appointment_date')+'T'+request.POST.get('appointment_time')
        appointment_time = datetime(*[int(v) for v in appointment_time.replace('T', '-').replace(':', '-').split('-')])
        appointment = Appointment(patient=patient, doctor=doctor, receptionist=request.user, case=c, appointment_time=appointment_time)
        appointment.save()
    return HttpResponseRedirect('/home')


#RETRIEVE
@login_required
def view(request):
    c = {}
    user = request.user
    if hasGroup(user, 'receptionist'):
        c['appointments'] = Appointment.objects.all()
    elif hasGroup(user, 'patient'):
        c['appointments'] = Appointment.objects.filter(patient=user)
    elif hasGroup(user, 'doctor'):
        c['appointments'] = Appointment.objects.filter(doctor=user)
    return render(request, 'appointments/view_all.html', c)


#UPDATE
@login_required
def changeAppointment(request, id):
    user = request.user
    if hasGroup(user, 'receptionist'):
        c = {'appointment': Appointment.objects.get(pk=id)}
        c.update(csrf(request))
        return render(request, 'appointments/change.html', c)
    return HttpResponseRedirect('/home')

@login_required
def doChange(request):
    user = request.user
    if hasGroup(user, 'receptionist'):
        appointment = Appointment.objects.get(pk=int(request.POST.get('id')))
        appointment.patient = User.objects.get(username=request.POST.get('patient', ''))
        appointment.doctor = User.objects.get(username=request.POST.get('doctor', ''))
        #appointment.appointment_time = datetime(*[int(v) for v in request.POST.get('appointment_time').replace('T', '-').replace(':', '-').split('-')])
        appointment.save()
    return HttpResponseRedirect('/home')

#DELETE
def delete(request, id):
    user = request.user
    if hasGroup(user, 'receptionist'):
        Appointment.objects.get(id=id).delete()
    return HttpResponseRedirect('/home')
