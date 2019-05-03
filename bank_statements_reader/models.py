# django
from django.db import models
# python
import csv
from datetime import date, datetime
from decimal import Decimal


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
    
    
    
    @staticmethod
    def read_bradesco_statement_csv(csv_file):
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

class BankStatementReader(models.Model):
    """
    Reads a statement csv file and process it to create
    the Year, Month and Transaction models
    """
    # TODO
    