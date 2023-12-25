from decimal import Decimal

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func
from model import Expenses, Incomes, Accounts, DefaultAccount
from config import Config


class BudgetController:
    def __init__(self):
        self.engine = create_engine(Config.DATABASE_URI)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def add_expense(self, year, month, category, amount, account_id):
        account = self.session.query(Accounts).get(account_id)

        # Create an expense object with provided data
        expense = Expenses(
            year=year,
            month=month,
            category=category,
            amount=amount,
            account_id=account_id
        )

        # Calculate total_expenses based on the values in Expenses
        total_expenses_in_year = (
            self.session.query(func.coalesce(func.sum(Expenses.amount), 0))
            .filter_by(year=year)
            .scalar()
        )
        total_expenses_in_month = (
            self.session.query(func.coalesce(func.sum(Expenses.amount), 0))
            .filter_by(year=year, month=month)
            .scalar()
        )

        # Update the Total Expenses fields in the Incomes table
        total_left_entry = (
            self.session.query(Incomes)
            .filter_by(year=year, month=month)
            .first()
        )
        if total_left_entry:
            total_left_entry.total_expenses_in_year = total_expenses_in_year
            total_left_entry.total_expenses_in_month = total_expenses_in_month

        account.balance -= Decimal(str(amount))

        # Add the expense to the session and commit the changes
        self.session.add(expense)
        self.session.commit()

    def add_income(self, year, month, exchange_rate, income_usd, account_id, additional_income=0.00):
        # Get the account by ID
        account = self.session.query(Accounts).get(account_id)

        if account:
            # Create an income object with provided data
            income = Incomes(
                year=year,
                month=month,
                exchange_rate=exchange_rate,
                income_usd=income_usd,
                account_id=account_id,  # Make sure to associate the correct account ID
                additional_income=additional_income
            )

            # Calculate additional fields based on the given logic
            income.income_uah = income_usd * exchange_rate
            income.single_tax = 0.05 * income.income_uah  # Single Tax is 5%
            income.ssc = 1474.00
            income.total_taxes = income.single_tax + income.ssc
            income.clean_income = income.income_uah - income.total_taxes
            income.total_left = income.clean_income + additional_income

            # Update the balance in the Accounts table
            account.balance += Decimal(str(income.total_left))

            # Add the income to the session and commit the changes
            self.session.add(income)
            self.session.commit()
        else:
            print("Account not found!")

    def modify_expense(self, expense_id, new_year, new_month, new_amount, new_category):
        try:
            # Modify the amount of an existing expense
            expense = self.session.query(Expenses).get(expense_id)
            if expense:
                # Calculate the change in amount
                amount_change = Decimal(str(new_amount)) - Decimal(str(expense.amount))

                # Update the Total Expenses in Year and Total Expenses in Month fields in the Incomes table
                total_expenses_in_year = (
                    self.session.query(func.coalesce(func.sum(Expenses.amount), 0))
                    .filter_by(year=expense.year)
                    .scalar()
                )
                total_expenses_in_month = (
                    self.session.query(func.coalesce(func.sum(Expenses.amount), 0))
                    .filter_by(year=expense.year, month=expense.month)
                    .scalar()
                )

                # Update the Total Expenses fields in the Incomes table
                total_left_entry = (
                    self.session.query(Incomes)
                    .filter_by(year=expense.year, month=expense.month)
                    .first()
                )
                if total_left_entry:
                    total_left_entry.total_expenses_in_year = total_expenses_in_year
                    total_left_entry.total_expenses_in_month = total_expenses_in_month

                # Modify the expense amount and commit the changes
                expense.year = new_year
                expense.month = new_month
                expense.amount = new_amount
                expense.category = new_category
                self.session.commit()

                # Update the balance in the Accounts table
                expense.account.balance -= amount_change
                self.session.commit()  # Commit the balance change separately
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error modifying expense: {e}")

    def delete_expense(self, expense_id):
        try:
            # Delete an existing expense
            expense = self.session.query(Expenses).get(expense_id)
            if expense:
                # Update the Total Expenses in Year and Total Expenses in Month fields in the Incomes table
                total_expenses_in_year = (
                    self.session.query(func.coalesce(func.sum(Expenses.amount), 0))
                    .filter_by(year=expense.year)
                    .scalar()
                )
                total_expenses_in_month = (
                    self.session.query(func.coalesce(func.sum(Expenses.amount), 0))
                    .filter_by(year=expense.year, month=expense.month)
                    .scalar()
                )

                # Update the Total Expenses fields in the Incomes table
                total_left_entry = (
                    self.session.query(Incomes)
                    .filter_by(year=expense.year, month=expense.month)
                    .first()
                )
                if total_left_entry:
                    total_left_entry.total_expenses_in_year = total_expenses_in_year
                    total_left_entry.total_expenses_in_month = total_expenses_in_month

                # Update the balance in the Accounts table
                expense.account.balance += expense.amount  # Revert the amount

                # Delete the expense and commit the changes
                self.session.delete(expense)
                self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error deleting expense: {e}")

    def modify_income(self, income_id, new_year, new_month, new_exchange_rate, new_income_usd, new_additional_income):
        try:
            # Modify the income amount of an existing income
            income = self.session.query(Incomes).get(income_id)
            if income:
                # Calculate existing total_left
                old_total_left = income.total_left

                # Calculate additional fields based on the given logic
                income.year = new_year
                income.month = new_month
                income.exchange_rate = new_exchange_rate
                income.income_usd = new_income_usd
                income.additional_income = new_additional_income
                income.income_uah = new_income_usd * income.exchange_rate
                income.single_tax = 0.05 * income.income_uah  # Single Tax is 5%
                income.total_taxes = float(income.single_tax) + float(income.ssc)
                income.clean_income = income.income_uah - income.total_taxes
                income.total_left = income.clean_income + income.additional_income

                # Update the balance in the Accounts table
                income.account.balance += Decimal(str(income.total_left)) - Decimal(str(old_total_left))

                # Commit the changes
                self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error modifying income: {e}")

    def delete_income(self, income_id):
        # Delete an existing income
        income = self.session.query(Incomes).get(income_id)
        if income:
            # Update the balance in the Accounts table
            income.account.balance -= Decimal(str(income.total_left))

            # Delete the income and commit the changes
            self.session.delete(income)
            self.session.commit()

    def get_incomes(self, year, month):
        incomes = (
            self.session.query(Incomes)
            .filter_by(year=year, month=month)
            .all()
        )
        return incomes

    def get_all_incomes(self):
        all_incomes = self.session.query(Incomes).all()
        return all_incomes

    def get_total_left(self, year, month):
        total_left = (
            self.session.query(Incomes.total_left)
            .filter_by(year=year, month=month)
            .scalar()
        )
        return total_left

    def get_total_expenses_by_category(self, year, category):
        total_expenses_by_category = (
            self.session.query(func.coalesce(func.sum(Expenses.amount), 0))
            .filter_by(year=year, category=category)
            .scalar()
        )
        return total_expenses_by_category

    def get_total_expenses_by_month(self, year, month):
        total_expenses_by_month = (
            self.session.query(func.coalesce(func.sum(Expenses.amount), 0))
            .filter_by(year=year, month=month)
            .scalar()
        )
        return total_expenses_by_month

    def get_total_expenses_in_year(self, year):
        total_expenses_in_year = (
            self.session.query(func.coalesce(func.sum(Expenses.amount), 0))
            .filter_by(year=year)
            .scalar()
        )
        return total_expenses_in_year

    def get_all_expenses(self):
        all_expenses = self.session.query(Expenses).all()
        return all_expenses


class AccountController:
    def __init__(self):
        self.engine = create_engine(Config.DATABASE_URI)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def create_account(self, name, currency):
        account = Accounts(name=name, currency=currency, balance=0)

        self.session.add(account)
        self.session.commit()

    def get_account_by_id(self, account_id):
        return self.session.get(Accounts, account_id)

    def get_all_accounts(self):
        all_accounts = self.session.query(Accounts).all()
        return all_accounts

    def delete_account(self, account_id):
        account = self.session.query(Accounts).get(account_id)

        if account:
            # Update expenses with the default account
            default_account = self.session.query(DefaultAccount).first()
            expenses_to_update = self.session.query(Expenses).filter_by(account_id=account_id).all()

            for expense in expenses_to_update:
                expense.account_id = default_account.id

            # Delete the original account
            self.session.delete(account)
            self.session.commit()
        else:
            print("Account not found!")

    def modify_account(self, account_id, new_name, new_currency, new_balance):
        # Modify the account information
        account = self.session.query(Accounts).get(account_id)
        if account:
            # Calculate additional fields based on the given logic
            account.name = new_name
            account.currency = new_currency
            account.balance = new_balance

            # Commit the changes
            self.session.commit()
