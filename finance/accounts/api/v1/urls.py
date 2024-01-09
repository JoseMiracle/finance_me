from django.urls import path
from finance.accounts.api.v1.views import (
    SignUpAPIView, 
    VerifyAccountAPIView,
    IntialSignInAPIView,
    FinalSignInAPIView,    
)

urlpatterns = [
    path('sign-up/', SignUpAPIView.as_view(), name='sign_up'),
    path('verify_account/<uidb64>/<token>/', VerifyAccountAPIView.as_view(), name='verify_account'),
    path('initial-sign-in/', IntialSignInAPIView.as_view(), name='initial_sign_in'),
    path('final-sign-in/', FinalSignInAPIView.as_view(), name='final_sign_in'),
]