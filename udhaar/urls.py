from django.urls import path
from .views import udhaar_home

urlpatterns = [
    path('', udhaar_home, name='udhaar'),
]