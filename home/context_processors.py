from django.contrib.auth.models import Group

def hasGroup(user, groupName):
    group = Group.objects.get(name=groupName)
    return True if group in user.groups.all() else False

def menu_processor(request):
    menu = {}
    menu['Profile'] = ''
    menu['Logout'] = ''
    user = request.user
    if hasGroup(user, 'doctor'):
        menu['Appointment'] = ''
        menu['MyCases'] = ''
    elif hasGroup(user, 'patient'):
        menu['Reports'] = ''
        menu['Appointment'] = ''
        menu['Medication'] = ''
        menu['Bills'] = ''
    elif hasGroup(user, 'receptionist'):
        menu['NewPatient'] = ''
        menu['ManageAppointments'] = ''
        menu['GenerateCase'] = ''
        menu['Bills'] = ''
    elif hasGroup(user, 'lab_attendant'):
        menu['Reports'] = ''
        menu['GenerateReport'] = ''
    elif hasGroup(user, 'inventory_manager'):
        menu['AllStock'] = ''
        menu['StockDetails'] = ''

    return {'menu': menu}
