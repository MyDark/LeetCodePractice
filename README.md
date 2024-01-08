Kotobudget: An Accounting Tool
==============================

Models
------

### Currency
Represents a type of currency.

*   **Code:** A short code (max length: 3, unique).
*   **Name:** The full name of the currency (max length: 255).


### Account
Represents a financial account, such as a bank or cash account.

*   **Name:** A name for the account (max length: 255).
*   **Description:** Additional information about the account (optional).
*   **Currency:** The type of currency used in the account.
*   **Balance:** The current balance of the account (max digits: 20, decimal places: 2, default: 0).


### Transaction
Represents a financial transaction, capturing details of income, expense, or transfer between accounts.

*   **Timestamp:** The date and time of the transaction.
*   **Account:** The account involved in the transaction.
*   **Transaction Type:** The type of transaction (Income, Expense, Transfer).
*   **Amount:** The monetary amount of the transaction (max digits: 10, decimal places: 2, default: 0.00).
*   **Currency:** The currency used in the transaction.
*   **Description:** Additional details about the transaction (optional).


### ExchangeRate
Represents exchange rates for different currencies.

*   **Timestamp:** The date and time when the exchange rate is recorded.
*   **Name:** A name or identifier for the exchange rate (max length: 255).
*   **Currency:** The currency for which the exchange rate is defined.
*   **Rate:** The exchange rate value (max digits: 10, decimal places: 4, default: 38.0775).


### TaxRule
Represents a rule for calculating taxes.

*   **Name:** A name or identifier for the tax rule (max length: 255).
*   **Description:** Additional details about the tax rule.
*   **Tax Type:** The type of tax calculation (Percentage, Fixed Amount, default: Percentage).
*   **Percentage:** The percentage value for tax calculation (max digits: 5, decimal places: 2, default: 5.00, optional).
*   **Fixed Amount:** A fixed amount for tax calculation (max digits: 6, decimal places: 2, default: 1562.00, optional).


### Transfer
Represents a transfer of money between two accounts, possibly in different currencies.

*   **Timestamp:** The date and time of the transfer.
*   **Source Account:** The account from which the money is transferred.
*   **Destination Account:** The account to which the money is transferred.
*   **Amount:** The monetary amount of the transfer (max digits: 10, decimal places: 2, default: 0.00).
*   **Source Currency:** The currency used in the source account.
*   **Destination Currency:** The currency used in the destination account.
*   **Exchange Rate:** The exchange rate applied to the transfer.
*   **Description:** Additional details about the transfer (optional).


### Usage
#### Install required packages:
`pip install -r requirements.txt`

#### Apply migrations:
`python manage.py makemigrations`
`python manage.py migrate`

#### Create superuser:
`python manage.py createsuperuser`

#### Run the development server:
`python manage.py runserver`
