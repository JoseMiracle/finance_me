from django.urls import path
from finance.accounts.api.v1.views import (
    SignUpAPIView, 
    VerifyOtpAPIView,
    IntialSignInAPIView,
    FinalSignInAPIView
)

urlpatterns = [
    path('sign-up/', SignUpAPIView.as_view(), name='sign_up'),
    path('verify-account/', VerifyOtpAPIView.as_view(), name='verify_account'),
    path('initial-sign-in/', IntialSignInAPIView.as_view(), name='initial_sign_in'),
    path('final-sign-in/', FinalSignInAPIView.as_view(), name='final_sign_in')
]