from django.urls import path

from . import views

urlpatterns = [
    path('ROUTE/', VIEW.as_view(), name=''),
]