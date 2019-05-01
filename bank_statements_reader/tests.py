from django.test import TestCase

from .models import Month, Transaction

from datetime import date

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
            flow_method="Visa Electron", date=date(19,1,2), month=Month.objects.get(month_number="1")
        )
        Transaction.objects.create(
            origin="Ponto Verde Supermer", statement_number="0300645", amount="-31.68",
            flow_method="Visa Electron", date=date(19,1,2), month=Month.objects.get(month_number="1")
        )
        Transaction.objects.create(
            origin="Panilha Delicates", statement_number="0090626", amount="-17.99",
            flow_method="Visa Electron", date=date(19,2,11), month=Month.objects.get(month_number="1")
        )

    def test_month_instance(self):
        january = Month.objects.get(month_number="1")
        self.assertEqual(january.month_number, "1")

    def test_transactions_link(self):
        january = Month.objects.get(month_number="1")
        self.assertEqual(january.transactions.count(), 3)