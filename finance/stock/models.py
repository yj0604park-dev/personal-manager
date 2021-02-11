import math

from django.db import models
from django.utils.translation import gettext_lazy as _


# Text Choices
class TransferType(models.TextChoices):
    DEPOSIT = "DEPOSIT", _("Deposit")
    WITHDRAW = "WITHDRAW", _("Withdraw")


class TradeType(models.TextChoices):
    BUY = "BUY", _("Buy")
    SELL = "SELL", _("Sell")


class CurrencyType(models.TextChoices):
    USD = "USD", _("USD")
    KRW = "KRW", _("KRW")


class AccountTypeChoices(models.TextChoices):
    """계좌 종류."""

    Saving = "Saving", _("입출금")
    Periodic = "Periodic", _("적금")
    Deposit = "Deposit", _("예금")


class BankType(models.TextChoices):
    """은행 종류."""

    Bank = "은행", _("Bank")
    Securities = "증권사", _("Securities")
    Insurance = "보험사", _("Insurance")
    Crypto = "암호화폐", _("Crypocurrency")


# Models
class Bank(models.Model):
    """은행."""

    name = models.CharField(max_length=40)
    bank_type = models.CharField(
        max_length=10, choices=BankType.choices, default=BankType.Bank
    )

    def __str__(self):
        return str(self.name)


class Saving(models.Model):
    """적금 계좌."""

    date = models.DateField()
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=100)
    principal = models.IntegerField()
    interest = models.IntegerField()
    is_tax_exemption = models.BooleanField()
    is_deposit = models.BooleanField(default=False)
    range = models.IntegerField(default=12)

    @property
    def interest_rate(self):
        """이자율."""
        return float(self.interest) / float(self.principal)

    @property
    def tax_rate(self):
        """세율."""
        if self.is_tax_exemption:
            return 0.014
        else:
            return 0.154

    @property
    def tax(self):
        """세금."""
        return math.floor(float(self.interest) * self.tax_rate)

    @property
    def interest_minus_tax(self):
        """세금 제외 이자."""
        return self.interest - self.tax

    @property
    def payment(self):
        """실지금액."""
        return self.principal + self.interest_minus_tax

    @property
    def interest_rate_minus_tax(self):
        """실지급 기준 이자율."""
        return self.interest_minus_tax / float(self.principal)

    @property
    def interest_rate_per_year(self):
        """연환산 이자율."""
        return math.pow(1.0 + self.interest_rate_minus_tax, 1.0 / self.range * 12) - 1.0


class StockPrice(models.Model):
    trade_date = models.DateTimeField()
    trade_type = models.CharField(max_length=10, choices=TradeType.choices)
    trade_amount = models.FloatField()
    trade_price = models.FloatField()
    trade_currency = models.CharField(
        max_length=3, choices=CurrencyType.choices, default=CurrencyType.KRW
    )

    fee = models.FloatField()
    fee_currency = models.CharField(
        max_length=3, choices=CurrencyType.choices, default=CurrencyType.KRW
    )

    def trade_price_w_currency(self):
        return f"{self.trade_price} {self.trade_currency}"

    trade_price_w_currency.short_description = "Trade Price"

    def fee_w_currency(self):
        return f"{self.fee} {self.fee_currency}"

    fee_w_currency.short_description = "Fee"


class Transfer(models.Model):
    """계좌 이체 내역."""

    date = models.DateTimeField()
    transfer_type = models.CharField(choices=TransferType.choices, max_length=10)


class Exchange(models.Model):
    """환전."""

    date = models.DateTimeField()
    from_amount = models.FloatField()
    to_amount = models.FloatField()
    from_currency = models.CharField(
        max_length=3, choices=CurrencyType.choices, default=CurrencyType.KRW
    )
    to_currency = models.CharField(
        max_length=3, choices=CurrencyType.choices, default=CurrencyType.USD
    )

    def get_currency_rate(self):
        """환율 계산."""
        return self.from_amount / self.to_amount


class Account(models.Model):
    """계좌 정보."""

    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=100, null=True, blank=True)
    account_name = models.CharField(max_length=100)
    last_updated = models.DateTimeField(auto_now_add=True)
    account_type = models.TextField(
        max_length=30,
        choices=AccountTypeChoices.choices,
        default=AccountTypeChoices.Saving,
    )
    closed = models.BooleanField(default=False)

    def __str__(self):
        return "{} {}".format(self.bank, self.account_number)
