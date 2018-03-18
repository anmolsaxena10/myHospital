from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,Group
from .models import Patient
from django.template.context_processors import csrf

# Create your views here.
@login_required
def myProfile(request):
    return render(request, 'profiles/my_profile.html')

@login_required
def register(request):
    c = {}
    c.update(csrf(request))
    return render(request, 'profiles/register.html')

@login_required
def doRegister(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    contact_no = request.POST.get('contact_no')
    address = request.POST.get('address')
    dob = request.POST.get('dob')
    blood_group = request.POST.get('blood_group')
    patient = User.objects.create_user(username=username, password=password)
    patient.patient = Patient(contact_no=contact_no, address=address, dob=dob, blood_group=blood_group)
    patient.patient.save()
    patient.save()

    group = Group.objects.get(name='patient')
    group.user_set.add(patient)
    group.save()

    return HttpResponseRedirect('/home')
