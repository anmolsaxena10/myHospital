from django.contrib.auth.models import Group

def hasGroup(user, groupName):
    group = Group.objects.get(name=groupName)
    return True if group in user.groups.all() else False

def menu_processor(request):
    menu = {}
    user = request.user
    if hasGroup(user, 'doctor'):
        menu['Appointment'] = '/appointments'
        menu['MyCases'] = ''
    elif hasGroup(user, 'patient'):
        menu['Reports'] = ''
        menu['Appointment'] = '/appointments'
        menu['Medication'] = ''
        menu['Bills'] = ''
    elif hasGroup(user, 'receptionist'):
        menu['NewPatient'] = ''
        menu['ManageAppointments'] = '/appointments'
        menu['GenerateCase'] = ''
        menu['Bills'] = ''
    elif hasGroup(user, 'lab_attendant'):
        menu['Reports'] = ''
        menu['GenerateReport'] = ''
    elif hasGroup(user, 'inventory_manager'):
        menu['AllStock'] = ''
        menu['StockDetails'] = ''

    return {'menu': menu}
