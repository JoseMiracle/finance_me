"""
URL configuration for finance project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from finance.accounts.api.v1.views import InvalidLinkView, SuccessPageView
from finance.loans.api.v1.views import (
    RejectRequestAsGuarantorPage, 
    AcceptRequestAsGuarantorPage,
    
)
from drf_spectacular.views import (
    SpectacularAPIView, 
    SpectacularRedocView, 
    SpectacularSwaggerView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/accounts/', include('finance.accounts.api.v1.urls')),
    path('api/v1/loans/', include('finance.loans.api.v1.urls')),
    path('finance-me/invalid-link/', InvalidLinkView.as_view(), name='invalid_link'),
    path('finance-me/success/', SuccessPageView.as_view(), name='success'),
    path('finance-me/rejection-page/<uuid:loan_guarantor_id>/', RejectRequestAsGuarantorPage.as_view(), name='rejection-page'),
    path('finance-me/guarantor-accept-request/<uuid:loan_guarantor_id>/', AcceptRequestAsGuarantorPage.as_view(), name='accept-request'),

    # SWAGGER ENDPOINTS
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

