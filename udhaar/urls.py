from django.urls import path
from . import views

urlpatterns = [
    # Yahan 'udhaar_view' ko badal kar 'udhaar_home' kiya gaya hai
    path('', views.udhaar_home, name='udhaar'), 

    # ✅ Baki sab sahi hai
    path('delete/udhaar/<int:id>/', views.delete_udhaar, name='delete_udhaar'),
    path('delete/payment/<int:id>/', views.delete_payment, name='delete_payment'),
    path('delete/customer/<int:id>/', views.delete_customer, name='delete_customer'),
]