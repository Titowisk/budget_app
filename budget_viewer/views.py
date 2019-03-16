from django.shortcuts import render
from django.views.generic import ListView

from bank_statements_reader.models import Transaction

# Create your views here.

# budget_viewer/transactions.html
# - show all incomes/expenses by month;
# - allow in-place adding/editing category

class TransactionsView(ListView):
    model = Transaction
    template_name = "budget_viewer/transactions.html"
    context_object_name = "transactions_list"

