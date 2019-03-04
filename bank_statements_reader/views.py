from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import FormView, ListView

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


def handle_csv_file(csv_file):
    pair_flag = False
    
    for byte_row in csv_file:
        row = byte_row.decode(encoding='iso-8859-1', errors='strict')
        fields = row.split(";")
        temporary_fields = True
        try:    
            if (pair_flag):
                pair_flag = False
                # handles pair's second line
                if (fields[1] != "Total do Dia"):
                    transaction.origin = fields[1]
                transaction.print_flow()
                
            elif (fields[2].isdigit()): # if line has a document_number it means it will show the cash_flow information I want
                # handles pair's first line 
                print("Documento Numero: {0}".format(fields[2]))
               
                # creates a helper to assign to the Object Transaction
                temporary_fields = {
                    'amount': 0, 'origin': '', 'flow_method': '',
                    'date': '', 'flow_type': ''
                }
                transaction = Transaction()
                if (fields[4] != ""):
                    transaction.amount = format_amount(fields[4]) # expense
                    transaction.flow_type = '0'
                elif(fields[3] != ""):
                    transaction.amount = format_amount(fields[3]) # income
                    transaction.flow_type = '1'

                transaction.date = format_date(fields[0])
                transaction.flow_method = fields[1]
                transaction.save()
                pair_flag = True
        except IndexError: # rows have diferents number of fields
            pass

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
            handle_csv_file(file)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

# def upload_file(request):
#     if request.method == 'POST':
#         print("FOI POST")
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             print(request.FILES['file'])
#             return HttpResponseRedirect('/success/')
#         else:
#             print("Form não é válido")

#     else:
#         form = UploadFileForm()
    
#     return render(request, 'bank_statements_reader/csv_reader.html', {'form': form})


# page to show a sample of the read files
class ShowSampleView(ListView):
    template_name = "bank_statements_reader/sample_view.html"
    model = Transaction
    context_object_name = "transactions_list"