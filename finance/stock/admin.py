from django.contrib import admin

from finance.stock import models


# Register your models here.
@admin.register(models.StockPrice)
class StockPriceAdmin(admin.ModelAdmin):
    """주식 가격."""

    list_display = (
        "trade_date",
        "trade_type",
        "trade_amount",
        "trade_price_w_currency",
        "fee_w_currency",
    )


@admin.register(models.Exchange)
class ExchangeAdmin(admin.ModelAdmin):
    """환전 내역."""


@admin.register(models.Transfer)
class TransferAdmin(admin.ModelAdmin):
    """계좌 이체 내역."""


@admin.register(models.Account)
class AccountAdmin(admin.ModelAdmin):
    """계좌 정보."""
