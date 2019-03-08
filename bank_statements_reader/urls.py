from django.urls import path

from . import views

urlpatterns = [
    path('csv-file', views.ReadFilesView.as_view(), name='csv-file'),
    path('sample_statement_table', views.ShowSampleView.as_view(), name='sample-view')
    # path('csv-file', views.upload_file, name='csv-file'),
]