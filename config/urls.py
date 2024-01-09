"""
URL configuration for finance project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path,include
from finance.accounts.api.v1.views import InvalidLinkView, SuccessPageView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/accounts/', include('finance.accounts.api.v1.urls')),
    path('api/v1/loans/', include('finance.loans.api.v1.urls')),
    path('finance-me/invalid-link/', InvalidLinkView.as_view(), name='invalid_link'),
    path('finance-me/success/', SuccessPageView.as_view(), name='success')

]


