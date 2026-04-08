"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from dashboard.views import DashboardView
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.http import HttpResponse


def create_admin(request):
    if not User.objects.filter(username='admin_meher').exists():
        User.objects.create_superuser('meher-online', 'mehercomputing@gmail.com', 'Nepster#440')
        return HttpResponse("Admin Created Successfully!")
    return HttpResponse("Admin already exists.")

# 🔐 Root redirect (login ya dashboard)
def home_redirect(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


urlpatterns = [

    # Admin
    path('admin/', admin.site.urls),

    # Root (IMPORTANT 🔥)
    path('', home_redirect),

    # Accounts (login/logout)
    path('', include('accounts.urls')),

    # Dashboard
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    # Apps
    path('data/', include('data_entry.urls')),
    path('monthly/', include('monthly_summary.urls')),
    path('yearly/', include('yearly_summary.urls')),
    path('billing/', include('billing.urls')),
    path('expense/', include('expenses.urls')),

]