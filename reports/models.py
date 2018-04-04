from django.db import models
from case.models import case
from django.contrib.auth.models import User

# Create your models here.
class Report(models.Model):
	case = models.ForeignKey(case, on_delete=models.CASCADE, related_name='report_case')
	lab_attendant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='report_lab_attendant')
	generated_date = models.DateField()
	description = models.CharField(max_length=200)

	def __str__(self):
		return self.case
