from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, Group
from .models import case
from datetime import datetime
from home.context_processors import hasGroup
from appointments.models import Appointment
from django.contrib import messages
from stock.models import items
from bill.models import bill
# Create your views here.

#CREATE
@login_required
def generate(request):
    if hasGroup(request.user, 'receptionist'):
        c = {}
        c.update(csrf(request))
        c['patients'] = User.objects.filter(groups__name='patient')
        return render(request, 'case/generate.html', c)
    messages.add_message(request, messages.WARNING, 'Access Denied.')
    return HttpResponseRedirect('/home')

@login_required
def doGenerate(request):
    if hasGroup(request.user, 'receptionist'):
        patient = User.objects.get(username=request.POST.get('patient', ''))
        description = request.POST.get('description', '')
        filed_date = datetime.now()
        c = case(patient=patient, receptionist=request.user, description=description, filed_date=filed_date)
        c.save()

        item = items.objects.get(item_name='Consulting Charges')
        quantity = 1
        bill_date = datetime.now()
        bill_details = 'Basic Consulting Charges'
        ammount = item.sell_price*quantity
        b = bill(case=c, item=item, quantity=quantity, bill_date=bill_date, bill_details=bill_details, ammount=ammount)
        b.save()

        messages.add_message(request, messages.INFO, 'Successfully Generated Case')
        return HttpResponseRedirect('/appointments/book')
    messages.add_message(request, messages.WARNING, 'Access Denied.')
    return HttpResponseRedirect('/home')

#RETRIEVE
@login_required
def view(request):
    c = {}
    user = request.user
    cases = None
    if hasGroup(user, 'receptionist'):
        cases = case.objects.all()
    elif hasGroup(user, 'patient'):
        cases = case.objects.filter(patient=user)
    elif hasGroup(user, 'doctor'):
        c['isDoctor'] = True
        cases = [appointment.case for appointment in Appointment.objects.filter(doctor=user)]

    open=[]
    closed=[]
    for ca in cases:
        if ca.closed_date:
            closed.append(ca)
        else:
            open.append(ca)
    c['openCases'] = open
    c['closedCases'] = closed
    return render(request, 'case/view.html', c)

#UPDATE
@login_required
def close(request, id):
    user = request.user
    if hasGroup(user, 'doctor'):
        c = case.objects.get(id=id)
        c.closed_date = datetime.now()
        c.save()
        messages.add_message(request, messages.INFO, 'Successfully Closed Case')
        return HttpResponseRedirect('/case')
    messages.add_message(request, messages.WARNING, 'Access Denied.')
    return HttpResponseRedirect('/home')


#DELETE
@login_required
def delete(request, id):
    user = request.user
    if hasGroup(user, 'receptionist'):
        case.objects.get(id=id).delete()
        messages.add_message(request, messages.INFO, 'Successfully Closed Case')
        return HttpResponseRedirect('/case')
    messages.add_message(request, messages.WARNING, 'Access Denied.')
    return HttpResponseRedirect('/home')
