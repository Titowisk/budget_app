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
    receiveis a GET request and returns months json data
    according to the year choosed.
    """
    def get(self, request, *args, **kwargs):
        print(kwargs['year'])
        months = Year.objects.get(name=kwargs['year']).months.all()
        months_display = list()
        for month in months:
            # {'id': 1,'name': Janeiro}, {'id': 2, 'name': Fevereiro}...
            months_display.append(dict(id=month.id, name=month.get_month_number_display()))
        data = dict()
        data['months'] = months_display
        return JsonResponse(data)

        


