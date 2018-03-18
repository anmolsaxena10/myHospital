from django.db import models
from case.models import case
from django.contrib.auth.models import User

# Create your models here.
class report(models.Model):
	case = models.ForeignKey(case, on_delete=models.CASCADE, related_name='report_case')
	lab_attendant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='report_lab_attendant')
	requested_date = models.DateField()
	generated_date = models.DateField()
	description = models.CharField(max_length=200)
