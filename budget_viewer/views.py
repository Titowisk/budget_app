from django.shortcuts import render
from django.views.generic import ListView
from django.http import JsonResponse

from bank_statements_reader.models import Transaction, Year, Month

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
        print(kwargs['year'])
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
        data_list = list()
        for t in transactions:
            data_list.append([t.origin, t.amount, t.flow_method])
        
        data = { # data formatting for DataTables structure
            "draw": 1,
            "recordsTotal": transactions.count(),
            "recordsFiltered": transactions.count(),
            "data": data_list
        }

        # https://docs.djangoproject.com/en/2.2/ref/request-response/#serializing-non-dictionary-objects
        return JsonResponse(data, safe=False)
            


        


