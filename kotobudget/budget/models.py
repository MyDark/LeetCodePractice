from django.db import models


class Account(models.Model):
    name = models.TextField()
    currency = models.TextField()
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)


class Expense(models.Model):
    year = models.IntegerField(default=2024)
    month = models.CharField(max_length=255, null=True)
    category = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_in_month = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_in_year = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)


class Income(models.Model):
    year = models.IntegerField(default=2024)
    month = models.CharField(max_length=255)
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    income_usd = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    income_uah = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    single_tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    ssc = models.DecimalField(max_digits=10, decimal_places=2, default=1474.00)
    total_taxes = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    clean_income = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    additional_income = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    expenses = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_left = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
