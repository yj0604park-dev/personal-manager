from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class StockPrice(models.Model):
    trade_date = models.DateTimeField()
    trade_type = models.CharField(max_length=10)
    trade_amount = models.FloatField()
    trade_price = models.FloatField()

    fee = models.FloatField()


class TransferType(models.TextChoices):
    DEPOSIT = "DEPOSIT", _("Deposit")
    WITHDRAW = "WITHDRAW", _("Withdraw")


class Transfer(models.Model):
    transfer_type = models.CharField(choices=TransferType.choices, max_length=10)
