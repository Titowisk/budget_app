from django.shortcuts import render
from django.views.generic import ListView, View
from django.http import JsonResponse, HttpResponse

from bank_statements_reader.models import Transaction, Year, Month
from .forms import CategoryForm


class YearsView(ListView):
    """
    Show the page transactions.html with years that contain
    months that contains existent transactions to be shwon.
    """
    model = Year
    template_name = "budget_viewer/transactions.html"
    context_object_name = "years"

class MonthsByYearList(ListView):
    """
    receiveis a GET request and returns ordered months json data
    according to the year choosed.
    """
    def get(self, request, *args, **kwargs):
        months = Year.objects.get(name=kwargs['year']).months.all()
        months_display = list()
        for month in sorted(months, key=lambda x: x.month_number):
            # {'id': 1,'name': Janeiro}, {'id': 2, 'name': Fevereiro}...
            months_display.append(dict(id=month.id, name=month.get_month_number_display()))
        data = dict()
        data['months'] = months_display
        return JsonResponse(data)

class transactionsByMonth(ListView):
    """
    receiveis a GET request and returns transactions json data
    according to the month choosed.
    """
    def get(self, request, *args, **kwargs):
        transactions = Month.objects.get(id=kwargs['month_id']).transactions.all()
        transactions_json = Transaction.serialize_to_json(transactions)
        # summary
        incomes_total = sum(t.amount for t in transactions if t.amount >= 0)
        expenses_total = sum(t.amount for t in transactions if t.amount < 0)
        summary_total = incomes_total + expenses_total
        summary = {"incomes_total": incomes_total, "expenses_total": expenses_total, "summary_total": summary_total}
        data = dict()
        data['transactions'] = transactions_json
        data['summary'] = summary

        # https://docs.djangoproject.com/en/2.2/ref/request-response/#serializing-non-dictionary-objects
        return JsonResponse(data, safe=False)
            
class EditCategoryEvent(View):

    def get(self, request, *args, **kwargs):
        print("INICIO GET")
        print(kwargs)
        # receiveis the pk
        row_pk = int(kwargs['row_pk'])
        transaction_to_be_edited = Transaction.objects.get(pk=row_pk)
        # get the form
        form = CategoryForm()
        raw_select_form = str(form['category'])
        # the selected option will be the current transaction's category (if exists)
        if (transaction_to_be_edited.category is not None):
            index = raw_select_form.find('value="{val}"'.format(transaction_to_be_edited.category))
            select_form = raw_select_form[: index] + 'selected' + raw_select_form[index - 1:]
            return HttpResponse(select_form)
        # return the html form to be inserted in popover
        else:

            return HttpResponse(raw_select_form)
    
    # def post(self, request, *args, **kwargs):
    #     # edit all similar transactions or only the selected one
    #     # checks if the edit will be for only one or all similars
    #     # if only one
    #     # find transaction by pk and update its category
    #     # else
    #     # find all transactions with the same origin and update its category
    #     # handle success and error
    #     pass


        


