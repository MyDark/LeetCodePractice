from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO
from controller import BudgetController, AccountController
from config import Config

app = Flask(__name__)
socketio = SocketIO(app)
app.config["SQLALCHEMY_DATABASE_URI"] = Config.DATABASE_URI
app.config["SERVER_NAME"] = "127.0.0.1:5000"
budget_controller = BudgetController()
account_controller = AccountController()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/incomes')
def incomes():
    accounts = account_controller.get_all_accounts()
    incomes = budget_controller.get_all_incomes()
    return render_template('incomes.html', accounts=accounts, incomes=incomes)


@app.route('/expenses')
def expenses():
    accounts = account_controller.get_all_accounts()
    expenses = budget_controller.get_all_expenses()
    return render_template('expenses.html', accounts=accounts, expenses=expenses)


@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        # Add a new expense
        year = int(request.form['year'])
        month = request.form['month']
        category = request.form['category']
        amount = float(request.form['amount'])
        account_id = int(request.form['account_id'])

        # Check if the account exists before adding income
        account = account_controller.get_account_by_id(account_id)
        if account:
            budget_controller.add_expense(year, month, category, amount, account_id)
            return redirect(url_for('expenses'))
        else:
            return "Account not found!", 404
    # If the request method is GET, fetch the list of accounts and existing incomes
    accounts = account_controller.get_all_accounts()
    expenses = budget_controller.get_all_expenses()  # You need to implement get_all_incomes() in your IncomeController

    return render_template('expenses.html', accounts=accounts, expenses=expenses)


@app.route('/add_income', methods=['GET', 'POST'])
def add_income():
    if request.method == 'POST':
        # Process the form data
        year = int(request.form['year'])
        month = request.form['month']
        exchange_rate = float(request.form['exchange_rate'])
        income_usd = float(request.form['income_usd'])
        additional_income = float(request.form['additional_income'])
        account_id = int(request.form['account_id'])

        # Check if the account exists before adding income
        account = account_controller.get_account_by_id(account_id)
        if account:
            budget_controller.add_income(year, month, exchange_rate, income_usd, account_id, additional_income)
            return redirect(url_for('incomes'))
        else:
            return "Account not found!", 404

    # If the request method is GET, fetch the list of accounts and existing incomes
    accounts = account_controller.get_all_accounts()
    incomes = budget_controller.get_all_incomes()  # You need to implement get_all_incomes() in your IncomeController

    return render_template('incomes.html', accounts=accounts, incomes=incomes)


@app.route('/delete_expense/<int:expense_id>')
def delete_expense(expense_id):
    # Delete an expense by ID
    budget_controller.delete_expense(expense_id)
    return redirect(url_for('expenses'))


@app.route('/modify_expense/<int:expense_id>', methods=['POST'])
def modify_expense(expense_id):
    # Modify the amount of an expense by ID
    new_year = request.form['new_year']
    new_month = request.form['new_month']
    new_amount = float(request.form['new_amount'])
    new_category = request.form['new_category']
    budget_controller.modify_expense(expense_id, new_year, new_month, new_amount, new_category)
    return redirect(url_for('expenses'))


@app.route('/delete_income/<int:income_id>')
def delete_income(income_id):
    # Delete an income by ID
    budget_controller.delete_income(income_id)
    return redirect(url_for('incomes'))


@app.route('/modify_income/<int:income_id>', methods=['POST'])
def modify_income(income_id):
    # Modify the income amount by ID
    new_exchange_rate = float(request.form['new_exchange_rate'])
    new_income_usd = float(request.form['new_income_usd'])
    new_additional_income = float(request.form['new_additional_income'])
    new_year = request.form['new_year']
    new_month = request.form['new_month']
    budget_controller.modify_income(income_id, new_year, new_month, new_exchange_rate, new_income_usd,
                                    new_additional_income)
    return redirect(url_for('incomes'))


@app.route('/accounts')
def accounts():
    get_accounts = account_controller.get_all_accounts()
    return render_template('accounts.html', accounts=get_accounts)


@app.route('/create_account', methods=['POST'])
def create_account():
    # Create a new account
    name = request.form['name']
    currency = request.form['currency']
    account_controller.create_account(name, currency)
    return redirect(url_for('accounts'))


@app.route('/delete_account/<int:account_id>')
def delete_account(account_id):
    # Delete an account by ID
    account_controller.delete_account(account_id)
    return redirect(url_for('accounts'))


@app.route('/modify_account/<int:account_id>', methods=['POST'])
def modify_account(account_id):
    # Modify the account information by ID
    new_name = request.form['new_name']
    new_currency = request.form['new_currency']
    new_balance = float(request.form['new_balance'])
    account_controller.modify_account(account_id, new_name, new_currency, new_balance)
    return redirect(url_for('accounts'))


@socketio.on('update_data')
def handle_update_data(message):
    # Triggered by the client to request updated data
    # Send the updated data to the client
    data = {
        'your_data': 'get_updated_data_from_controller'
    }
    socketio.emit('data_updated', data)


if __name__ == "__main__":
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)

# if __name__ == '__main__':
#     # app.run(host="0.0.0.0", port=5000)
#     app.run(debug=True)
