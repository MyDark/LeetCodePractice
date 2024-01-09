from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the budget index.")


class TransactionController:

    def __init__(self):
        pass

    def add_transaction(self):
        pass

    def modify_transaction(self):
        pass

    def delete_transaction(self):
        pass


class TransferController:

    def __init__(self):
        pass

    def add_transfer(self):
        pass

    def modify_transfer(self):
        pass

    def delete_transfer(self):
        pass


class AccountController:

    def __init__(self):
        pass

    def add_account(self):
        pass

    def modify_account(self):
        pass

    def delete_account(self):
        pass
