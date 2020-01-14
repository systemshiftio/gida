from django.db import models
import api.models as am
import investment.models as im

# Create your models here.

TRANSACTION_TYPE = (
    ('Investment', 'Investment'),
    ('Rent', 'Rent'),
    ('Withdrawal', 'Withdrawal')
)

STATUS = (
    ('SUCCESS', 'Success'),
    ('Failed', 'Failed')
)


class Transaction(models.Model):
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE)
    created = models.DateTimeField()
    trasaction_worth = models.DecimalField(max_digits=8, decimal_places=2)
    partment = models.ForeignKey(am.Apartment, null=True, on_delete=models.CASCADE)
    investment = models.ForeignKey(im.PersonalInvestment, null=True, on_delete=models.CASCADE)
    booking = models.ForeignKey(am.BookedApartment, null=True, on_delete=models.CASCADE)
    reference_id = models.CharField(max_length=50)
    status = models.CharField(max_length=15, choices=STATUS)