from django.contrib import admin
from .models import Account, Transaction, ExchangeRate, TaxRule, TaxPayment, Transfer

admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(ExchangeRate)
admin.site.register(TaxRule)
admin.site.register(TaxPayment)
admin.site.register(Transfer)

