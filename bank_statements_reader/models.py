# django
from django.db import models
# python
import csv
from datetime import date, datetime
from decimal import Decimal
from django.core import serializers

# Useful Links

## Models 
## https://docs.djangoproject.com/en/2.2/topics/db/models/

## Objects Manager
## https://docs.djangoproject.com/en/2.2/topics/db/managers/

## Model Instance Reference
## https://docs.djangoproject.com/en/2.2/ref/models/instances/

## Model Field Reference
## https://docs.djangoproject.com/en/2.2/ref/models/fields/

class CategoryNameException(Exception):
    """
    Custom Category Exceptions
    """
    DEFAULT_MESSAGE = "Only especific categories are allowed"

    def __init__(self, message=DEFAULT_MESSAGE):
        self.message = message
    


class CategoryManager(models.Manager):

    
    def create_category(self, name):
        """
        Category.objects.create_category(name="Food")

        Creates a Category object and saves it to the database
        """

        # checks if name matches one of the pre determined choices
        if ( any([name in category_choice for category_choice in Category.CATEGORIES]) ):
            category = self.create(name=name)
        # raises exception if no match occurs
        else:
            raise CategoryNameException()
        
        return category


class Category(models.Model):
    """
    Category model

    Categories: 
    Food, Entertainment, Transportation, HealthCare,
    Clothing, Utilities, Education, Supplies

    One Category can have many Transactions
    but each Transaction belongs only to one category 
    """

    CATEGORIES = [
        ('Food', 'Food'),
        ('Entertainment', 'Entertainment'),
        ('Transportation', 'Transportation'),
        ('HealthCare', 'HealthCare'),
        ('Clothing', 'Clothing'),
        ('Utilities', 'Utilities'),
        ('Education', 'Education'),
        ('Supplies', 'Supplies'),
    ]

    objects = CategoryManager()

    name = models.CharField(max_length=25, default=None, null=True, choices=CATEGORIES)
    # TODO bank_account

    TRANSLATION_PTBR = {
        'Food': 'Alimentação',
        'Entertainment': 'Lazer',
        'Transportation': 'Transporte',
        'HealthCare': 'Saúde',
        'Clothing': 'Vestimenta',
        'Utilities': 'Utilidades',
        'Education': 'Educação',
        'Supplies': 'Suprimentos',

    }

    def get_translation(category_name):
        """
        Receiveis a category name and returns the corresponding
        translation to portuguese (Brazillian)
        """
        return TRANSLATION_PTBR[category_name]

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
    """
    takes raw_date in DD/MM/YY
    returns YYYY-MM-DD
    """
    date_string = raw_date.split("/") # [23, 11, 1989]
    day = int(date_string[0])
    month = int(date_string[1])

    current_century = date.today().year // 100 * 100 # 1989 -> 1900, 2019 -> 2000
    year = int(date_string[2]) + current_century
    print(year)
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
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, related_name='categories') #if category is deleted, the transactions still exists

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
    def serialize_to_json(query):
        """
        Takes a DJango query and serialize it to json data format
        Ex:
        q1 = Transaction.objects.filter(amount__gte= Decimal(100))
        data = serializers.serialize("json", q1)
        [{
            "model": "bank_statements_reader.transaction",
            "pk": 790,
            "fields": {
                "statement_number": "4191977",
                "origin": "Remet.vitor Rabelo Filardi",
                "amount": "562.00",
                "flow_method": " Ted Csal p/ccor",
                "date": "0018-12-05",
                "slug": "",
                "month": null
            }
        }, {
            "model": "bank_statements_reader.transaction",
            "pk": 791,
            "fields": {
                "statement_number": "4192088",
                "origin": "Remet.vitor Rabelo Filardi",
                "amount": "562.00",
                "flow_method": " Ted Csal p/ccor",
                "date": "0018-12-05",
            }
            ...
        ]
        """
        # https://docs.djangoproject.com/en/2.2/topics/serialization/
        choosen_fields = ("statement_number", "date", "flow_method", "origin", "amount")
        return serializers.serialize("json", query, fields=choosen_fields)

    
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
    
    def identify_category_by_transaction_description():
        Transaction.objects.all()

    