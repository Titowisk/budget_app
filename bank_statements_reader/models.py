# django
from django.db import models
# python
from datetime import date


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
