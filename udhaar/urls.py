from django.urls import path
from .views import udhaar_home, delete_customer

urlpatterns = [
    path('', udhaar_home, name='udhaar'),
    path('delete/customer/<int:id>', delete_customer, name='delete_customer'),
]