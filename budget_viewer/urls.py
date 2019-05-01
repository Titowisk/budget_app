from django.urls import path

from . import views

urlpatterns = [
    path('transactions', views.TransactionsView.as_view(), name='transactions'),
]