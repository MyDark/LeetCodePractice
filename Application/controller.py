from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func
from model import Expenses, Incomes
from config import Config


class BudgetController:
    def __init__(self):
        self.engine = create_engine(Config.DATABASE_URI)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def add_expense(self, year, month, category, amount):
        # Create an expense object with provided data
        expense = Expenses(year=year, month=month, category=category, amount=amount)

        # Get the Total Left from the Incomes table for the specified year and month
        total_left = (
            self.session.query(Incomes)
            .filter_by(year=year, month=month)
            .with_entities(Incomes.total_left)
            .scalar()
        )

        # Update the Total Expenses in Year and Total Expenses in Month fields in the Incomes table
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

        # Add the expense to the session and commit the changes
        self.session.add(expense)
        self.session.commit()

    def add_income(self, year, month, exchange_rate, income_usd, additional_income=0.00):
        # Create an income object with provided data
        income = Incomes(year=year, month=month, exchange_rate=exchange_rate, income_usd=income_usd)

        # Calculate additional fields based on the given logic
        income.income_uah = income_usd * exchange_rate
        income.single_tax = 0.05 * income.income_uah  # Single Tax is 5%
        income.ssc = 1474.00
        income.total_taxes = income.single_tax + income.ssc
        income.clean_income = income.income_uah - income.total_taxes
        income.additional_income = additional_income
        income.total_left = income.clean_income + income.additional_income - income.total_taxes

        # Add the income to the session and commit the changes
        self.session.add(income)
        self.session.commit()

    def modify_expense(self, expense_id, new_amount):
        # Modify the amount of an existing expense
        expense = self.session.query(Expenses).get(expense_id)
        if expense:
            # Update the Total Left from the Incomes table for the specified year and month
            total_left = (
                self.session.query(Incomes)
                .filter_by(year=expense.year, month=expense.month)
                .with_entities(Incomes.total_left)
                .scalar()
            )

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
            expense.amount = new_amount
            self.session.commit()

    def delete_expense(self, expense_id):
        # Delete an existing expense
        expense = self.session.query(Expenses).get(expense_id)
        if expense:
            # Update the Total Left from the Incomes table for the specified year and month
            total_left = (
                self.session.query(Incomes)
                .filter_by(year=expense.year, month=expense.month)
                .with_entities(Incomes.total_left)
                .scalar()
            )

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

            # Delete the expense and commit the changes
            self.session.delete(expense)
            self.session.commit()

    def modify_income(self, income_id, new_income_usd):
        # Modify the income amount of an existing income
        income = self.session.query(Incomes).get(income_id)
        if income:
            # Calculate additional fields based on the given logic
            income.income_usd = new_income_usd
            income.income_uah = new_income_usd * income.exchange_rate
            income.single_tax = 0.05 * income.income_uah  # Single Tax is 5%
            income.total_taxes = income.single_tax + income.ssc
            income.clean_income = income.income_uah - income.total_taxes
            income.total_left = income.clean_income + income.additional_income - income.total_taxes

            # Commit the changes
            self.session.commit()

    def delete_income(self, income_id):
        # Delete an existing income
        income = self.session.query(Incomes).get(income_id)
        if income:
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


controller = BudgetController()

#############  Add expenses  #############
# controller.add_expense(2023, 'April', 'Food', 2000)

#############  GET EXPENSES  #############
# # Get total expenses by category
# total_expenses_food_2023 = controller.get_total_expenses_by_category(2023, 'Food')
# print(f"Total Expenses for Food in 2023: {total_expenses_food_2023}")
# # Get total expenses by month
# total_expenses_april_2023 = controller.get_total_expenses_by_month(2023, 'April')
# print(f"Total Expenses in April 2023: {total_expenses_april_2023}")
# # Get total expenses in the year
# total_expenses_2023 = controller.get_total_expenses_in_year(2023)
# print(f"Total Expenses in 2023: {total_expenses_2023}")


#############  Add incomes  #############
# controller.add_income(2023, 'April', 36.5686, 300.00)

#############  GET INCOMES  #############
incomes = controller.get_incomes(2023, 'April')
for income in incomes:
    print(f"Income (USD): {income.income_usd}")
    print(f"Income (UAH): {income.income_uah}")
    print(f"Single Tax: {income.single_tax}")
    print(f"SSC: {income.ssc}")
    print(f"Total Taxes: {income.total_taxes}")
    print(f"Clean Income (UAH): {income.clean_income}")
    print(f"Additional Income: {income.additional_income}")
    print(f"Total Left: {income.total_left}")

# total_left_for_april_2023 = controller.get_total_left(2023, 'April')
# print(f"Total Left for April 2023: {total_left_for_april_2023}")
