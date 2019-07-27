from decimal import Decimal as D

from django.shortcuts import render
from django.views.generic import TemplateView
from django.db.models import Avg, Sum

from bank_statements_reader.models import Year, Month, Transaction

import plotly.graph_objects as go
from plotly.offline import plot

# Aggregation Django
# https://docs.djangoproject.com/en/2.2/topics/db/aggregation/

# Filter look up reference
# https://docs.djangoproject.com/en/2.2/ref/models/querysets/#django.db.models.query.QuerySet

def get_year_desc():
    """
    Query all year objects of a user
    """
    return Year.objects.all().order_by('-name')

def get_months_by_year(year_id):
    """
    Query all month objects by a selected year
    returns a ordered asc month objects list 

    year_id: a int number
    """
    return Month.objects.filter(year__id=year_id).order_by('month_number')

def convert_to_verbose_months(month_objects):
    """
    Turn a list of Month objects into a list
    of verbose name months
    """
    MONTHS = {
        "1": "Jan", "2": "Fev", "3": "Mar", "4": "Abr", "5": "Mai", "6": "Jun",
        "7": "Jul", "8": "Ago", "9": "Set", "10": "Out", "11": "Nov", "12": "Dez" 
    }
    return [MONTHS[month.month_number] for month in month_objects]

def get_transactions_sum_data(month_objects, amount_type):
    """
    Query transactions data for charts
    returns a list of aggregate sum of transactions by month.

    month_objects: a list of Month objects ordered by month_number
    amount_type: either a 'expenses' or 'incomes' string.
    """
    if (amount_type == 'expenses'):
        chart_data = [
            result['amount__sum'].quantize(D('0.01')).copy_abs()
            if result['amount__sum'] != None
            else 0
            for result in 
            [month.transactions.filter(amount__lte=0).aggregate(Sum('amount')) for month in month_objects]
        ]
    elif (amount_type == 'incomes'):
        chart_data =  [
            result['amount__sum'].quantize(D('0.01')).copy_abs() 
            if result['amount__sum'] != None
            else 0
            for result in 
            [month.transactions.filter(amount__gt=0).aggregate(Sum('amount')) for month in month_objects]
        ]
    
    return chart_data

def create_income_expense_scatter_plot(year_id):
    """
    Creates a plotly scattter chart using transactions of each month
    of a selected year.

    year_id: int number
    """
    
    month_objects = get_months_by_year(year_id)
    
    # build chart data 
    months =  convert_to_verbose_months(month_objects)

    y_expenses = get_transactions_sum_data(month_objects, amount_type='expenses')
    
    y_incomes = get_transactions_sum_data(month_objects, amount_type='incomes')
    
    # buids scatter-chart
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
        scatter_plot = create_income_expense_scatter_plot(kwargs['year_pk'])
        
        context['scatter_plot'] = scatter_plot
        context['by_income'] = True
        context['years'] = get_year_desc()
        return self.render_to_response(context)