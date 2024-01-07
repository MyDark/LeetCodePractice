from django.db import models


class Account(models.Model):
    """
    Represents a financial account, such as a bank account or a cash account.
    """
    name = models.CharField(max_length=255)
    currency = models.CharField(max_length=3)
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

    timestamp = models.DateTimeField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=2, choices=TransactionType.choices)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    currency = models.CharField(max_length=3)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} {self.currency}"


class ExchangeRate(models.Model):
    """
    Represents exchange rates for different currencies.
    """
    timestamp = models.DateTimeField()
    name = models.CharField(max_length=255)
    currency = models.CharField(max_length=3)
    rate = models.DecimalField(max_digits=10, decimal_places=4, default=0.0000)

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
    percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, blank=True, null=True)
    fixed_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, blank=True, null=True)

    def __str__(self):
        return self.name


class TaxPayment(models.Model):
    """
    Represents a payment made for taxes based on a specific tax rule.
    """
    timestamp = models.DateTimeField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='tax_payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    currency = models.CharField(max_length=3)
    tax_rule = models.ForeignKey(TaxRule, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Tax Payment - {self.amount} {self.currency}"


class Transfer(models.Model):
    """
    Represents a transfer of money between two accounts, possibly in different currencies.
    """
    timestamp = models.DateTimeField()
    source_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='source_transfers')
    destination_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='destination_transfers')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    source_currency = models.CharField(max_length=3)
    destination_currency = models.CharField(max_length=3)
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=4, default=1.0000)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Transfer - {self.amount} {self.source_currency} to {self.destination_currency}"

