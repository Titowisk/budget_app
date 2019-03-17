from django.shortcuts import render
from django.views.generic import ListView

from bank_statements_reader.models import Transaction

# budget_viewer/transactions.html
# - show all incomes/expenses by month;
# - allow in-place adding/editing category

def get_active_months_years():
    """
    This functions creates a year_month_dict
    'year': [months] Ex: 2019: [1,2,3,7], 2018: [1,2,3,4,5,6,7,8]
    so I can show a table by year and month
    """
    transactions_list = Transaction.objects.all()
    year_month_dict = dict() # 'year': [months] Ex: 2019: [1,2,3,7], 2018: [1,2,3,4,5,6,7,8]
    for t in transactions_list:
        if (t.date.year in year_month_dict.keys()):
            year_month_dict[t.date.year].append(t.date.month)
        else:
            year_month_dict.setdefault(t.date.year, [])
    return year_month_dict

class TransactionsView(ListView):
    model = Transaction
    template_name = "budget_viewer/transactions.html"
    context_object_name = "transactions_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data( **kwargs)
        year_month_dict = get_active_months_years()
        context['year_month_dict'] = year_month_dict
        return context

