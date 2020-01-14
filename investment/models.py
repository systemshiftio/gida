from django.db import models
import api.models as am
from django.contrib.postgres.fields import JSONField
# Create your models here.

LOCATION = (
     ('Yaba', 'Yaba'),
     ('Lekki', 'Lekki'),
     ('Victoria-Island', 'Victoria-Island'),
     ('Surulere', 'Surulere'),
     ('Ikoyi', 'Ikoyi')
 )

STATE = (
    ('Abuja', 'Abuja'),
    ('Lagos', 'Lagos')
 )

class Apartment(models.Model):
    roi = models.IntegerField()
    investment_time = models.IntegerField(default=6)
    description = models.TextField()
    images = JSONField(default=list)
    state = models.CharField(max_length=50, choices=STATE)
    location = models.CharField(max_length=50, choices=LOCATION)
    status = models.BooleanField(default=True)
    min_investment = models.DecimalField(max_digits=9, decimal_places=2)
    

class PersonalInvestment(models.Model):
    owner = models.ForeignKey(am.GidaUser, on_delete=True)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    principal = models.DecimalField(max_digits=9, decimal_places=2)
    current_value = models.DecimalField(max_digits=9, decimal_places=2)
    maturity_period = models.DateField()
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)