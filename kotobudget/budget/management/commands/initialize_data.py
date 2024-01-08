from django.core.management.base import BaseCommand
from django.utils import timezone
from kotobudget.budget.models import Currency, Account, Transaction, ExchangeRate, TaxRule, Transfer


class Command(BaseCommand):
    help = 'Initialize sample data and perform transactions'

    def handle(self, *args, **options):
        # Create sample accounts
        currency_usd = Currency.objects.create(code='USD', name='US Dollar')
        currency_eur = Currency.objects.create(code='EUR', name='Euro')

        account1 = Account.objects.create(name='Account 1', currency=currency_usd, balance=1000.00)
        account2 = Account.objects.create(name='Account 2', currency=currency_eur, balance=500.00)

        # Perform transactions
        income_transaction = Transaction.objects.create(
            timestamp=timezone.now(),
            account=account1,
            transaction_type=Transaction.TransactionType.INCOME,
            amount=500.00,
            currency=currency_usd,
            description='Salary'
        )

        # Create an exchange rate between USD and EUR
        exchange_rate_usd_to_eur = ExchangeRate.objects.create(
            timestamp=timezone.now(),
            name='USD to EUR',
            currency=currency_usd,
            rate=0.85  # Example exchange rate
        )

        # Perform a transfer with exchange rate consideration
        transfer_transaction = Transfer.objects.create(
            timestamp=timezone.now(),
            source_account=account1,
            destination_account=account2,
            amount=100.00,
            source_currency=currency_usd,
            destination_currency=currency_eur,
            exchange_rate=exchange_rate_usd_to_eur.rate,
            description='Transfer between accounts'
        )

        expense_transaction = Transaction.objects.create(
            timestamp=timezone.now(),
            account=account1,
            transaction_type=Transaction.TransactionType.EXPENSE,
            amount=200.00,
            currency=currency_usd,
            description='Groceries'
        )

        # Calculate and perform tax payment
        # Example tax rule with 5% of income
        percentage_tax_rule = TaxRule.objects.create(
            name='5% of Income',
            description='5% of the income tax rule',
            tax_type=TaxRule.TaxType.PERCENTAGE,
            percentage=5.00,
        )

        # Example tax rule with a fixed amount of 1562 UAH
        fixed_amount_tax_rule = TaxRule.objects.create(
            name='Fixed Amount Tax',
            description='Fixed amount tax rule',
            tax_type=TaxRule.TaxType.FIXED_AMOUNT,
            fixed_amount=1562.00,
        )

        # Use the correct tax rule for calculation
        tax_amount = income_transaction.amount * (percentage_tax_rule.percentage / 100)

        transfer_amount_in_source_currency = transfer_transaction.amount * transfer_transaction.exchange_rate
        account1.balance -= transfer_transaction.amount
        account2.balance += transfer_amount_in_source_currency
        account1.save()
        account2.save()

        # Print account balances after transactions
        self.stdout.write(f'Account 1 Balance: {account1.balance} {account1.currency.code}')
        self.stdout.write(f'Account 2 Balance: {account2.balance} {account2.currency.code}')
