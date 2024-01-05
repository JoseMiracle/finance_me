from django.urls import path
from finance.loans.api.v1.views import (
    RequestableLoanAmountAPIView,
    RequestForLoanAPIView,
    GuarantorDecisonAPIView,
    AdminGetLoanRequestAPIView,
    AdminApproveLoanRequestAPIView
)

urlpatterns = [
    path('requestable-loan-amount/', RequestableLoanAmountAPIView.as_view(), name='requestable_loan_amount'),
    path('request-for-loan/', RequestForLoanAPIView.as_view(), name='request_for_loan'),
    path('guarantor-decision/<uuid:loan_guarantor_id>/', GuarantorDecisonAPIView.as_view(), name='guarantor_decision'),
    path('loan-requests/', AdminGetLoanRequestAPIView.as_view(), name='all-loans'),
    path('approve-loan/<uuid:loan_id>/', AdminApproveLoanRequestAPIView.as_view(), name='approve_loan'),
]