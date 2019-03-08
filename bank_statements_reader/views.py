from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import FormView, ListView
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from .forms import UploadFileForm
from .models import Transaction

import csv
from datetime import date
from decimal import Decimal

# talvez seja util https://django-import-export.readthedocs.io/en/latest/index.html

def format_amount(amount):
    # takes amount as a string and return as a Decimal
    # 1.124,00
    # amount = amount.strip('"').replace(".", "") # amount comes with between "", why? I don't know
    # digits, decimals = [float(n) for n in amount.split(",")] # [321, 12]
    amount = amount.replace(".", "").replace(",", ".").strip('"quit')
    
    return Decimal(float(amount))

def format_date(raw_date):
    # takes raw_date in DD/MM/YYYYY
    # returns YYYY-MM-DD
    day, month, year = [int(date_string) for date_string in raw_date.split("/")]
    return date(year, month, day)


def read_csv_file(csv_file):
    pair_flag = False
    list_of_transactions = []
    ## creates a helper to assign to the Object Transaction
    transaction = dict()
    for byte_row in csv_file:
        row = byte_row.decode(encoding='iso-8859-1', errors='strict')
        fields = row.split(";")
        # the info about the transaction comes in a pair of 2 different lines that repeat themselves through the document
        try:    
            if (pair_flag):
                pair_flag = False
                # handles pair's second line
                if (fields[1] != "Total do Dia"):
                    transaction['origin'] = fields[1]

                list_of_transactions.append(transaction)
                # print(transaction.items()) # debug

            elif (fields[2].isdigit()): # if line has a document_number it means it will show the cash_flow information I want
                # handles pair's first line 
                # print("Documento Numero: {0}".format(fields[2])) # debug 
                
                ## empty the dict for each new transction
                transaction = dict()
                transaction['statement_number'] = fields[2] # statement_number = ex. 0948731
                if (fields[4] != ""):
                    transaction['amount'] = format_amount(fields[4]) # expense
                elif(fields[3] != ""):
                    transaction['amount'] = format_amount(fields[3]) # income

                transaction['date'] = format_date(fields[0])
                transaction['flow_method'] = fields[1]
                pair_flag = True
        except IndexError: # rows have diferents number of fields
            pass
        
    return list_of_transactions

def create_transaction(transaction_dict):
    # checks if statement_number already exists in db
    try:
        Transaction.objects.get(statement_number=transaction_dict['statement_number']) # raises DoesNotExist error if not found
        
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
    except MultipleObjectsReturned:
        # if statement_number is unique, then this should never happen!!
        print("===== |OH GOD, PLEASE DON'T LET THIS HAPPEN| =====")

    

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
            transactions = read_csv_file(file)
            for t_dict in transactions:
                create_transaction(t_dict)

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
