from django.test import TestCase

from .models import Month

class MonthModelTests(TestCase):
    # https://docs.djangoproject.com/en/2.2/topics/testing/overview/
    # https://docs.djangoproject.com/en/2.2/intro/tutorial05/

    def setUp(self):
        Month.objects.create(month_number="1")

    def create_month_instance(self):
        january = Month.objects.get(month_number="1")
        self.assertEqual(january.month_number, "1")

