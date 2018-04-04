from django.contrib.auth.models import Group

def hasGroup(user, groupName):
    group = Group.objects.get(name=groupName)
    return True if group in user.groups.all() else False

def menu_processor(request):
    menu = {}
    user = request.user
    if hasGroup(user, 'doctor'):
        menu['Appointment'] = '/appointments'
        menu['MyCases'] = '/case'
    elif hasGroup(user, 'patient'):
        menu['Reports'] = '/reports'
        menu['Appointment'] = '/appointments'
        menu['Medication'] = ''
        menu['Bills'] = ''
        menu['MyCases'] = '/case'
    elif hasGroup(user, 'receptionist'):
        menu['NewPatient'] = '/profile/register'
        menu['ManageAppointments'] = '/appointments'
        menu['NewAppointment'] = '/appointments/book'
        menu['Bills'] = ''
        menu['GenerateCase'] = '/case/generate'
    elif hasGroup(user, 'lab_attendant'):
        menu['Reports'] = '/reports'
        menu['GenerateReport'] = '/reports/generate'
    elif hasGroup(user, 'inventory_manager'):
        menu['AllStock'] = ''
        menu['StockDetails'] = ''

    return {'menu': menu}
