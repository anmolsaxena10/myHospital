from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,Group
from .models import Patient
from django.template.context_processors import csrf
from home.context_processors import hasGroup
from django.contrib import messages

# Create your views here.
@login_required
def myProfile(request):
    c={}
    if hasGroup(request.user, 'patient'):
        c['isPatient'] = True
    return render(request, 'profiles/my_profile.html', c)

@login_required
def register(request):
    if hasGroup(request.user, 'receptionist'):
        c = {}
        c.update(csrf(request))
        return render(request, 'profiles/register.html')
    else:
        messages.add_message(request, messages.WARNING, 'Access Denied.')
        return HttpResponseRedirect('/home')

@login_required
def doRegister(request):
    if hasGroup(request.user, 'receptionist'):
        username = request.POST.get('username')
        if User.objects.filter(username=username).exists():
            messages.add_message(request, messages.ERROR, 'Username Already Exists.')
            return HttpResponseRedirect('/profile/register')
        password = request.POST.get('password1')
        cpassword = request.POST.get('password2')
        if not password == cpassword:
            messages.add_message(request, messages.ERROR, 'Passwords not matching.')
            return HttpResponseRedirect('/profile/register')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        contact_no = request.POST.get('contact_no')
        if not contact_no.isdigit():
            messages.add_message(request, messages.ERROR, 'Wrong Contact no.')
            return HttpResponseRedirect('/profile/register')
        address = request.POST.get('address')
        dob = request.POST.get('dob')
        blood_group = request.POST.get('blood_group')
        email = request.POST.get('email')
        patient = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, email=email)
        patient.patient = Patient(contact_no=int(contact_no), address=address, dob=dob, blood_group=blood_group)
        patient.patient.save()
        patient.save()

        group = Group.objects.get(name='patient')
        group.user_set.add(patient)
        group.save()

        messages.add_message(request, messages.WARNING, 'Successfully Registered '+username)
        return HttpResponseRedirect('/case/generate')
    else:
        messages.add_message(request, messages.WARNING, 'Access Denied.')
        return HttpResponseRedirect('/home')
