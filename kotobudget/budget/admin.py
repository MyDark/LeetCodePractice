from django.contrib import admin
from .models import Currency, Account, Transaction, ExchangeRate, TaxRule, Transfer

admin.site.register(Currency)
admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(ExchangeRate)
admin.site.register(TaxRule)
admin.site.register(Transfer)

