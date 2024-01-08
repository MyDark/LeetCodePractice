from django.db import models


class Currency(models.Model):
    """
    Represents a currency.
    """
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} - {self.name}"


class Account(models.Model):
    """
    Represents a financial account, such as a bank account or a cash account.
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    """
    Represents a financial transaction, capturing details of income, expense, or transfer between accounts.
    """

    class TransactionType(models.TextChoices):
        INCOME = 'IN', 'Income'
        EXPENSE = 'EX', 'Expense'
        TRANSFER = 'TR', 'Transfer'

    timestamp = models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=2, choices=TransactionType.choices)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} {self.currency}"


class ExchangeRate(models.Model):
    """
    Represents exchange rates for different currencies.
    """
    timestamp = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    rate = models.DecimalField(max_digits=10, decimal_places=4, default=38.0775)

    def __str__(self):
        return f"{self.name} - {self.rate} {self.currency}"


class TaxRule(models.Model):
    """
    Represents a rule for calculating taxes.
    """
    class TaxType(models.TextChoices):
        PERCENTAGE = 'PER', 'Percentage'
        FIXED_AMOUNT = 'FIX', 'Fixed Amount'

    name = models.CharField(max_length=255)
    description = models.TextField()
    tax_type = models.CharField(max_length=3, choices=TaxType.choices, default=TaxType.PERCENTAGE)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, default=5.00, blank=True, null=True)
    fixed_amount = models.DecimalField(max_digits=6, decimal_places=2, default=1562.00, blank=True, null=True)

    def __str__(self):
        return self.name


class Transfer(models.Model):
    """
    Represents a transfer of money between two accounts, possibly in different currencies.
    """
    timestamp = models.DateTimeField(auto_now_add=True)
    source_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='source_transfers')
    destination_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='destination_transfers')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    source_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='source_transfers')
    destination_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='destination_transfers')
    exchange_rate = models.ForeignKey(ExchangeRate, on_delete=models.CASCADE, related_name='transfers')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Transfer - {self.amount} {self.source_currency} to {self.destination_currency}"
