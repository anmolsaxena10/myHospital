from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, Group
from .models import Appointment
from datetime import datetime
from home.context_processors import hasGroup
# Create your views here.
@login_required
def book(request):
    c = {}
    c.update(csrf(request))
    c['patients'] = User.objects.filter(groups__name='patient')
    c['doctors'] = User.objects.filter(groups__name='doctor')
    return render(request, 'appointments/book_appointment.html', c)

@login_required
def doBook(request):
    user = request.user
    if hasGroup(user, 'receptionist'):
        patient = User.objects.get(username=request.POST.get('patient', ''))
        doctor = User.objects.get(username=request.POST.get('doctor', ''))
        appointment_time = request.POST.get('appointment_date')+'T'+request.POST.get('appointment_time')
        appointment_time = datetime(*[int(v) for v in appointment_time.replace('T', '-').replace(':', '-').split('-')])
        appointment = Appointment(patient=patient, doctor=doctor, receptionist=request.user, appointment_time=appointment_time)
        appointment.save()
    return HttpResponseRedirect('/home')

@login_required
def view(request):
    c = {}
    user = request.user
    if hasGroup(user, 'receptionist'):
        c['appointments'] = Appointment.objects.all()
    else:
        c['appointments'] = Appointment.objects.filter(patient=user)
    return render(request, 'appointments/view_all.html', c)

@login_required
def changeAppointment(request, id):
    user = request.user
    if hasGroup(user, 'receptionist'):
        c = {'appointment': Appointment.objects.get(pk=id)}
        return render(request, 'appointments/change.html', c)
    return HttpResponseRedirect('/home')

@login_required
def doChange(request):
    
