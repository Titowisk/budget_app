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

# Filter look up reference
# https://docs.djangoproject.com/en/2.2/ref/models/querysets/#django.db.models.query.QuerySet

# class AnalisysView(TemplateView):
#     template_name = "analasys_view/analisys.html"
    
    
#     def get_context_data(self, **kwargs):
#         context = super(TemplateView, self).get_context_data(**kwargs)
#         context['years'] = Year.objects.all().order_by('-name')
#         return context

def get_year_desc():
    """
    TODO
    """
    return Year.objects.all().order_by('-name')

def create_scatter_plot_by_year(year_id):
    """
    TODO
    """
    MONTHS = {
        1: "Jan", 2: "Fev", 3: "Mar", 4: "Abr", 5: "Mai", 6: "Jun",
        7: "Jul", 8: "Ago", 9: "Set", 10: "Out", 11: "Nov", 12: "Dez" 
        }
    # year_objects = Year.objects.all().order_by('-name') # - orders by DESC
    month_objects = Month.objects.filter(year__id=year_id).order_by('month_number')
    
    # x_axis =  [MONTHS[month.month_number] for month in month_objects]
    months =  [MONTHS[int(month.month_number)] for month in month_objects]

    # y_axis = [
    #     result['amount__sum'].quantize(D('0.01')).copy_abs() for result in 
    #     [month.transactions.filter(amount__lte=0).aggregate(Sum('amount')) for month in month_objects]
    #     ]
    y_expenses = [
        result['amount__sum'].quantize(D('0.01')).copy_abs()
        if result['amount__sum'] != None
        else 0
        for result in 
        [month.transactions.filter(amount__lte=0).aggregate(Sum('amount')) for month in month_objects]
        ]
    
    y_incomes = [
        result['amount__sum'].quantize(D('0.01')).copy_abs() 
        if result['amount__sum'] != None
        else 0
        for result in 
        [month.transactions.filter(amount__gt=0).aggregate(Sum('amount')) for month in month_objects]
        ]
    
    # get plotly.offline
    # fig = go.Figure(data=go.Scatter(x=x_axis, y=y_axis))
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=months, y=y_expenses, name="Gastos",
        line=dict(color='firebrick', width=4)
    ))
    
    fig.add_trace(go.Scatter(
        x=months, y=y_incomes, name="Rendas",
        line=dict(color='#22b222', width=4)
    ))

    fig.update_layout(
        title='Gastos e Rendas do Ano XXXX', 
        xaxis_title='Meses',
        yaxis_title='Agregado por mês'
        )

    # render chart in a context
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)

    return plot_div

class AnalisysByIncomeView(TemplateView):
    """
    TODO
    """
    template_name = "analasys_view/analisys_by_income.html"
    # get data
    
    def get_context_data(self, **kwargs):
        """
        TODO
        """
        context = super(TemplateView, self).get_context_data(**kwargs)
       
        context['years'] = get_year_desc()
        context['by_income'] = True
        return context


class AnalisysByIncomePerYearView(TemplateView):
    """
    TODO
    """
    template_name = "analasys_view/analisys_by_income.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        scatter_plot = create_scatter_plot_by_year(kwargs['year_pk'])
        
        context['scatter_plot'] = scatter_plot
        context['by_income'] = True
        context['years'] = get_year_desc()
        return self.render_to_response(context)