from django.urls import path, include
from .views import *

app_name = 'customers'

urlpatterns = [
    path('home', CustomerListView.as_view(), name='customer-list-view'),
    path('test/', render_pdf_view, name='test-view'),
    path('pdf/<pk>/', customer_render_pdf_view, name='customer-pdf-view'),
    path('send', index),
]