"""
URL configuration for finance project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/accounts/', include('finance.accounts.api.v1.urls')),
    path('api/v1/loans/', include('finance.loans.api.v1.urls'))
]
