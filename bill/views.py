from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, Group
from .models import bill
from stock.models import items, stock
from datetime import datetime
from home.context_processors import hasGroup
from case.models import case
from django.contrib import messages
# Create your views here.

#CREATE
@login_required
def generate(request, case_id):
    if hasGroup(request.user, 'doctor'):
        c = {}
        c.update(csrf(request))
        c['case'] = case.objects.get(id=int(case_id))
        c['items'] = items.objects.all()
        return render(request, 'bill/generate.html', c)
    messages.add_message(request, messages.WARNING, 'Access Denied.')
    return HttpResponseRedirect('home/')

@login_required
def doGenerate(request):
    if hasGroup(request.user, 'doctor'):
        c = case.objects.get(id=request.POST.get('case', ''))
        item = items.objects.get(id=request.POST.get('item', ''))
        quantity = int(request.POST.get('quantity', ''))
        bill_date = datetime.now()
        bill_details = request.POST.get('description', '')
        ammount = item.sell_price * quantity
        b = bill(case=c, item=item, quantity=quantity, bill_date=bill_date, bill_details=bill_details, ammount=ammount)
        b.save()
        messages.add_message(request, messages.INFO, 'Successfully Added Medicine.')
        return HttpResponseRedirect('/case/')
    messages.add_message(request, messages.WARNING, 'Access Denied.')
    return HttpResponseRedirect('/home/')

#RETRIEVE
@login_required
def view(request):
    c = {}
    c.update(csrf(request))
    if hasGroup(request.user, 'patient'):
        c['bills'] = []
        c['isPatient'] = True
        for cases in case.objects.filter(patient=request.user):
            c['bills'].extend(list(bill.objects.filter(case=cases)))
    elif hasGroup(request.user, 'receptionist'):
        id = request.POST.get('patient', '')
        if id == '':
            c['selectPatient'] = True
            c['patients'] = User.objects.filter(groups__name='patient')
            return render(request, 'bill/view_bill.html', c)
        else:
            c['bills'] = []
            for cases in case.objects.filter(patient=User(id=id)):
                c['bills'].extend(list(bill.objects.filter(case=cases)))
    else:
        messages.add_message(request, messages.WARNING, 'Access Denied.')
        return HttpResponseRedirect('/home')

    bills = c['bills']
    c['paidBills'] = []
    c['pendingBills'] = []
    for b in bills:
        if b.is_paid:
            c['paidBills'].append(b)
        else:
            c['pendingBills'].append(b)
    return render(request, 'bill/view_bill.html', c)

@login_required
def viewMedicine(request):
    c = {}
    if hasGroup(request.user, 'patient'):
        c['bills'] = []
        c['isPatient'] = True
        for cases in case.objects.filter(patient=request.user):
            c['bills'].extend(list(bill.objects.filter(case=cases)))
        return render(request, 'bill/medicines.html', c)
    else:
        messages.add_message(request, messages.WARNING, 'Access Denied.')
        return HttpResponseRedirect('/home')

#UPDATE
@login_required
def pay(request):
    user = request.user
    if hasGroup(user, 'receptionist'):
        ids = request.POST.getlist('ids','123')
        if type(ids)==type([]):
            for id in ids:
                b = bill.objects.get(id=int(id))
                b.is_paid = True
                b.save()
        else:
            b = bill.objects.get(id=int(ids))
            b.is_paid = True
            b.save()
        messages.add_message(request, messages.INFO, 'Bill Paid Successfully.')
        return HttpResponseRedirect('/bill/')
    messages.add_message(request, messages.WARNING, 'Access Denied.')
    return HttpResponseRedirect('/home')

#DELETE
@login_required
def delete(request, id):
    user = request.user
    if hasGroup(user, 'receptionist'):
        bill.objects.get(id=id).delete()
        messages.add_message(request, messages.INFO, 'Successfully Deleted Bill.')
        return HttpResponseRedirect('/bill/')
    messages.add_message(request, messages.WARNING, 'Access Denied.')
    return HttpResponseRedirect('/home')
