from django.test import TestCase

from .models import Year, Month, Transaction, Category, CategoryNameException

from datetime import date
import decimal
import json

class CategoryModelTests(TestCase):

    def setUp(self):
        Category.objects.create_category("Food")

    def test_category_instance(self):
        category = Category.objects.get(name="Food")
        self.assertEqual(category.name, "Food")
    
    def test_category_choices(self):
        with self.assertRaises(CategoryNameException):
            category = Category.objects.create_category("Weapons")
        


class TransactionModelTests(TestCase):
    
    def setUp(self):
        Transaction.objects.create(
            origin="Tagarelli", statement_number="0161503", amount="-17.03",
            flow_method="Visa Electron", date=date(2019,1,2)
        )
    
    def test_transaction_instance(self):
        expense = Transaction.objects.get(statement_number="0161503")
        self.assertEqual(expense.origin, "Tagarelli")
        self.assertEqual(str(expense.amount), "-17.03")
        self.assertEqual(expense.amount, decimal.Decimal("-17.03"))
        self.assertEqual(expense.flow_method, "Visa Electron")
        self.assertEqual(expense.date, date(2019,1,2))
        self.assertEqual(expense.category, None) # null category from database returns None in python
    
    def test_transaction_category(self):
        category_food = Category.objects.create_category("Food")
        expense = Transaction.objects.get(statement_number="0161503")
        category_food.transactions.add(expense)

        self.assertEqual(Category.objects.get(id=1).transactions.count(), 1) # Category can access Transaction
        self.assertEqual(expense.category.name, "Food") # Transaction can be add to Category
    
    def test_serialize_to_json(self):
        """
        [
            {"model": "bank_statements_reader.transaction", 
            "pk": 1, 
            "fields": {
                "statement_number": "0161503", 
                "origin": "Tagarelli", 
                "amount": "-17.03", 
                "flow_method": "Visa Electron", 
                "date": "2019-01-02", 
                "category": null
                }
            }
        """
        query = Transaction.objects.filter(statement_number="0161503")
        json_string = Transaction.serialize_to_json(query)
        self.assertTrue(isinstance(json_string, str)) # serialize returns a json string
        json_list = json.loads(json_string) # string must be a valid json
        json_python_object = json_list[0]
        self.assertEqual(json_python_object["model"], "bank_statements_reader.transaction")
        self.assertEqual(json_python_object["pk"], 1)
        self.assertEqual(json_python_object["fields"]["statement_number"], "0161503")
        

class MonthModelTests(TestCase):
    # https://docs.djangoproject.com/en/2.2/topics/testing/overview/
    # https://docs.djangoproject.com/en/2.2/intro/tutorial05/

    def setUp(self):
        """
        02/01/19; Visa Electron;0161503;;"-17,03";
        ;Tagarelli;;

        02/01/19; Visa Electron;0300645;;"-31,68";
        ;Ponto Verde Supermer;;

        11/02/19; Visa Electron;0090626;;"-17,99";
        ;Panilha Delicates;;
        """
        Month.objects.create(month_number="1")
        Transaction.objects.create(
            origin="Tagarelli", statement_number="0161503", amount="-17.03",
            flow_method="Visa Electron", date=date(2019,1,2), month=Month.objects.get(month_number="1")
        )
        Transaction.objects.create(
            origin="Ponto Verde Supermer", statement_number="0300645", amount="-31.68",
            flow_method="Visa Electron", date=date(2019,1,2), month=Month.objects.get(month_number="1")
        )
        Transaction.objects.create(
            origin="Panilha Delicates", statement_number="0090626", amount="-17.99",
            flow_method="Visa Electron", date=date(2019,2,11), month=Month.objects.get(month_number="1")
        )

    def test_month_instance(self):
        january = Month.objects.get(month_number="1")
        self.assertEqual(january.month_number, "1")

    def test_transactions_link(self):
        january = Month.objects.get(month_number="1")
        self.assertEqual(january.transactions.count(), 3)
    
    def test_month_display(self):
        january = Month.objects.get(month_number="1")
        self.assertEqual(january.get_month_number_display(), "Janeiro")


class YearModelTests(TestCase):

    def setUp(self):
        Year.objects.create(name=date(2019, 11, 2).year)
        Month.objects.create(month_number="1", year=Year.objects.get(name="2019"))
        Month.objects.create(month_number="3", year=Year.objects.get(name="2019"))
        Month.objects.create(month_number="5", year=Year.objects.get(name="2019"))
    
    def test_year_instance(self):
        year = Year.objects.get(name="2019")
        self.assertEqual(year.name, "2019")
    
    def test_months_link(self):
        year = Year.objects.get(name="2019")
        self.assertEqual(year.months.count(), 3)
        march = year.months.filter(month_number__contains="3")[0]
        self.assertEqual(march.month_number, "3")