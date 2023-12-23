from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from model import Expenses, Incomes
from controller import BudgetController
from config import Config

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = Config.DATABASE_URI
controller = BudgetController(Config.DATABASE_URI)


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

    return redirect(url_for('index'))


@app.route('/add_income', methods=['POST'])
def add_income():
    # Add a new income
    year = int(request.form['year'])
    month = request.form['month']
    exchange_rate = float(request.form['exchange_rate'])
    income_usd = float(request.form['income_usd'])
    additional_income = float(request.form['additional_income'])

    controller.add_income(year, month, exchange_rate, income_usd, additional_income)

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
