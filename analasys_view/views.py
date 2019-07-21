from decimal import Decimal as D

from django.shortcuts import render
from django.views.generic import TemplateView
from django.db.models import Avg, Sum

from bank_statements_reader.models import Year, Month, Transaction

import plotly.graph_objects as go
from plotly.offline import plot

# Create your views here.

# Aggregation Django
# https://docs.djangoproject.com/en/2.2/topics/db/aggregation/

class AnalisysByIncomeView(TemplateView):
    template_name = "analasys_view/analisys_by_income.html"
    # get data
    
    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data(**kwargs)
        # format data (sum expenses per month)
        # year_objects = Year.objects.all().order_by('-name') # - orders by DESC
        month_objects = Month.objects.filter(year__name='2019').order_by('month_number')
        
        x_axis =  [month.month_number for month in month_objects]

        y_axis = [
            result['amount__sum'].quantize(D('0.01')).copy_abs() for result in 
            [month.transactions.filter(amount__lte=0).aggregate(Sum('amount')) for month in month_objects]
            ]
        # y_axis = [month.transactions.filter(amount__lte=0).aggregate(Avg('amount')) for month in 2019_month_objects]
        
        # get plotly.offline
        fig = go.Figure(data=go.Scatter(x=x_axis, y=y_axis))

        # render chart in a context
        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        
        context['scatter_plot'] = plot_div
        return context
    