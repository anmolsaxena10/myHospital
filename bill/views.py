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
# Create your views here.

#CREATE
@login_required
def generate(request, case_id):
    if hasGroup(request.user, 'doctor'):
        c = {}
        c.update(csrf(request))
        c['case'] = case.objects.get(id=case_id)
        c['items'] = items.objects.all()
        return render(request, 'bill/generate.html', c)
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
    return HttpResponseRedirect('/home/')

#RETRIEVE
@login_required
def view(request):
    c = {}
    c.update(csrf(request))
    if hasGroup(request.user, 'patient'):
        c['bills'] = []
        for cases in case.objects.filter(patient=request.user):
            c['bills'].extend(list(bill.objects.filter(case=cases)))
    elif hasGroup(request.user, 'receptionist'):
        id = request.POST.get('patient', '')
        if id == '':
            c['selectPatient'] = True
            c['patients'] = User.objects.filter(groups__name='patient')
        else:
            c['bills'] = []
            for cases in case.objects.filter(patient=User(id=id)):
                c['bills'].extend(list(bill.objects.filter(case=cases)))
    return render(request, 'bill/view_bill.html', c)

@login_required
def viewMedicine(request):
    if hasGroup(request.user, 'patient'):
        pass

#UPDATE
@login_required
def pay(request):
    user = request.user
    if hasGroup(user, 'receptionist'):
        ids = request.POST.get('ids')
        for id in ids:
            b = bill.objects.get(id=int(id))
            b.is_paid = True
            b.save()
    return HttpResponseRedirect('/home')

#DELETE
@login_required
def delete(request, id):
    user = request.user
    if hasGroup(user, 'receptionist'):
        bill.objects.get(id=id).delete()
    return HttpResponseRedirect('/home')
