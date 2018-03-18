from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class items(models.Model):
	item_name = models.CharField(max_length=50)
	cost_price = models.IntegerField()
	sell_price = models.IntegerField()
	manufacturer = models.CharField(max_length=50)
	description = models.CharField(max_length=100)

class stock(models.Model):
	item_name = models.ForeignKey(items, on_delete=models.CASCADE, related_name='stock_item')
	quantity = models.IntegerField()
	purchase_date = models.DateField()
	expiry_date = models.DateField()
