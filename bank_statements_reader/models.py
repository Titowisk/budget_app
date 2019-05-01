# django
from django.db import models
# python
from datetime import date, datetime

class BankStatementReader(models.Model):
    # TODO
    pass

class Year(models.Model):
    """
    Year model, group months by year
    """
    def name_default():
        return datetime.now().year

    
    name = models.CharField(max_length=4, default=name_default)
    # TODO bankAccount = models.ForeignKey() each bankAccount will have years of transactions

    

class Month(models.Model):
    """
    Model month groups transactions by month
    """

    MONTH_CHOICES = (
        ("1", "Janeiro"), ("2", "Fevereiro"), ("3", "Março"), ("4", "Abril"), 
        ("5", "Maio"), ("6", "Junho"), ("7", "Julho"), ("8", "Agosto"), 
        ("9", "Setembro"), ("10", "Outubro"), ("11", "Novembro"), ("12", "Dezembro")
        )
    
    month_number = models.CharField(max_length=15, choices=MONTH_CHOICES)
    year = models.ForeignKey('Year', on_delete=models.CASCADE, related_name='months', null=True)

class Transaction(models.Model):

    # ?
    INCOME = '1'
    EXPENSE = '0'

    EXPENSE_OR_INCOME = (
        (EXPENSE, 'Expense'),
        (INCOME, 'Income')
    )

    # attributes
    statement_number = models.CharField(max_length=15, unique=True, null=True) # I think it's unique (remove null=True later)
    origin = models.CharField(max_length=100)
    amount = models.DecimalField(decimal_places=2, max_digits=9)
    flow_method = models.CharField(max_length=50)
    date = models.DateField()
    slug = models.SlugField()
    month = models.ForeignKey('Month', on_delete=models.SET_NULL, null=True, related_name='transactions') # if month is deleted, the transactions still exists

    # methods
    def print_flow(self):
        text = """
                ==================== CashFlow object ===================
                Amount: {amount}, Date: {date}, Flow_Method: {flow_method}
                Origin: {origin} 
                """.format(
                    amount = self.amount,
                    date = "{0}-{1}-{2}".format(self.date.day,self.date.month, self.date.year),
                    flow_method = self.flow_method,
                    origin = self.origin
                )
        print(text)
    
    def __str__(self):
        return self.origin
