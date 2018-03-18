from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class case(models.Model):
	patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='case_patient')
	receptionist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='case_receptionist')
	filed_date = models.DateField()
	closed_date = models.DateField()
