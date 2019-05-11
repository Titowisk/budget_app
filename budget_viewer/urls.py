from django.urls import path

from . import views
# https://docs.djangoproject.com/en/2.2/ref/urls/#path

urlpatterns = [
    path('transactions', views.YearsView.as_view(), name='transactions'),
    path('transactions/monthsByYear/<year>', views.MonthsByYearList.as_view(), name='months_by_year'),
    path('transactions/transactionsByMonth/<month_id>', views.transactionsByMonth.as_view(), name='transactions_by_month'),
]