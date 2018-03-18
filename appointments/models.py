from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Appointment(models.Model):
	patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointment_patient')
	receptionist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointment_receptionist')
	doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointment_doctor')
	appointment_time = models.DateTimeField()
