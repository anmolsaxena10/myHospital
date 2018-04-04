from django.db import models
from django.contrib.auth.models import User
from case.models import case

# Create your models here.
class Appointment(models.Model):
	patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointment_patient')
	receptionist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointment_receptionist')
	doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointment_doctor')
	case = models.ForeignKey(case, on_delete=models.CASCADE, related_name='appointment_case')
	appointment_time = models.DateTimeField()

	def __str__(self):
		return self.patient.username + ' with ' + self.doctor.username
