from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from model import Expenses, Incomes
from controller import BudgetController
from config import Config

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = Config.DATABASE_URI
controller = BudgetController()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/incomes')
def incomes():
    incomes = controller.get_all_incomes()
    return render_template('incomes.html', incomes=incomes)


@app.route('/expenses')
def expenses():
    expenses = controller.get_all_expenses()
    return render_template('expenses.html', expenses=expenses)


@app.route('/add_expense', methods=['POST'])
def add_expense():
    # Add a new expense
    year = int(request.form['year'])
    month = request.form['month']
    category = request.form['category']
    amount = float(request.form['amount'])

    controller.add_expense(year, month, category, amount)

    return redirect(url_for('expenses'))


@app.route('/add_income', methods=['POST'])
def add_income():
    # Add a new income
    year = int(request.form['year'])
    month = request.form['month']
    exchange_rate = float(request.form['exchange_rate'])
    income_usd = float(request.form['income_usd'])
    additional_income = float(request.form['additional_income'])

    controller.add_income(year, month, exchange_rate, income_usd, additional_income)

    return redirect(url_for('incomes'))


@app.route('/delete_expense/<int:expense_id>')
def delete_expense(expense_id):
    # Delete an expense by ID
    controller.delete_expense(expense_id)
    return redirect(url_for('expenses'))


@app.route('/modify_expense/<int:expense_id>', methods=['POST'])
def modify_expense(expense_id):
    # Modify the amount of an expense by ID
    new_amount = float(request.form['new_amount'])
    controller.modify_expense(expense_id, new_amount)
    return redirect(url_for('expenses'))


@app.route('/delete_income/<int:income_id>')
def delete_income(income_id):
    # Delete an income by ID
    controller.delete_income(income_id)
    return redirect(url_for('incomes'))


@app.route('/modify_income/<int:income_id>', methods=['POST'])
def modify_income(income_id):
    # Modify the income amount by ID
    new_exchange_rate = float(request.form['new_exchange_rate'])
    new_income_usd = float(request.form['new_income_usd'])
    new_additional_income = float(request.form['new_additional_income'])
    controller.modify_income(income_id, new_exchange_rate, new_income_usd, new_additional_income)
    return redirect(url_for('incomes'))


if __name__ == '__main__':
    app.run(debug=True)
