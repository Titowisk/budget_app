from django.urls import path

from . import views
# https://docs.djangoproject.com/en/2.2/ref/urls/#path

urlpatterns = [
    path('by_income', name='by_income'),
    path('by_category', name='by_category'),
    path('by_origin', name='by_origin')
]