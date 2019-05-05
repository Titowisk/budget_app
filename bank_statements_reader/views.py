from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import FormView, ListView
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from .forms import UploadFileForm
from .models import Transaction, Year, Month

import csv
from datetime import date
from decimal import Decimal

# talvez seja util https://django-import-export.readthedocs.io/en/latest/index.html

def create_transaction(transaction_dict):
    """
    Create a Transaction instance or return an existing one
    """
    # checks if statement_number already exists in db
    try:
        t = Transaction.objects.get(statement_number=transaction_dict['statement_number']) # raises DoesNotExist error if not found
        
    except ObjectDoesNotExist:
        # happens when the transaction is indeed new
        t = Transaction(
            statement_number = transaction_dict['statement_number'],
            origin = transaction_dict['origin'],
            amount = transaction_dict['amount'],
            flow_method = transaction_dict['flow_method'],
            date = transaction_dict['date']
        )
        t.save()
        return t
    except MultipleObjectsReturned:
        # if statement_number is unique, then this should never happen!!
        print("===== |OH GOD, PLEASE DON'T LET THIS HAPPEN| =====")

    return t

def create_year(year):
    """
    Create a Year object or return an existing one
    """
    year = str(year)
    try:
        y = Year.objects.get(name=year)
    except ObjectDoesNotExist:
        # if object doesn't exist, create a new one
        y = Year(name=year)
        y.save()
    
    return y

def create_month(month):
    """
    Create a Month object or return an existing one
    """
    month = str(month)
    try:
        m = Month.objects.get(month_number=month)
    except ObjectDoesNotExist:
        # if object doesn't exist, create a new one
        m = Month(month_number=month)
        m.save()
    
    return m

# landing-page to read files
class ReadFilesView(FormView):
    template_name = "bank_statements_reader/csv_reader.html"
    success_url = "sample_statement_table"
    form_class = UploadFileForm


    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        file = request.FILES['file']
        if form.is_valid():
            # transactions = read_csv_file(file)
            transactions = Transaction.read_bradesco_statement_csv(file)
            for t_dict in transactions:
                transaction = create_transaction(t_dict)
                year = create_year(t_dict['date'].year)
                month =  create_month(t_dict['date'].month)
                month.year = year # year has many months
                transaction.month = month # month has many transactions


            return self.form_valid(form)
        else:
            return self.form_invalid(form)


# page to show a sample of the read files
class ShowSampleView(ListView):
    template_name = "bank_statements_reader/sample_view.html"
    model = Transaction
    context_object_name = "transactions_list"

    # show the latest 15 records (ordered_by id) as a sample view
    def get_queryset(self):
        transactions = Transaction.objects.order_by('id')
        transactions = sorted(transactions, reverse=True, key=lambda x:x.id)
        return transactions[:15]
