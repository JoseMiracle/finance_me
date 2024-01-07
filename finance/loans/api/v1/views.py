from django.shortcuts import render
from rest_framework import generics, permissions, status
from finance.loans.api.v1.serializers import(
    RequestableLoanAmountSerializer,
    RequestForLoanSerializer,
    GuarantorDecisonSerializer,
)
from finance.loans.models import(
    RequestableLoanAmount,
    RequestForLoan,
    LoanGuarantor
)
from finance.loans.mails import loan_request_decision_mail
from rest_framework.response import Response


class RequestableLoanAmountAPIView(generics.ListCreateAPIView):
    serializer_class = RequestableLoanAmountSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = RequestableLoanAmount.objects.all()


    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs) 


class RequestForLoanAPIView(generics.CreateAPIView):
    serializer_class = RequestForLoanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    

class GuarantorDecisonAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class =  GuarantorDecisonSerializer

    def get_object(self):
        loan_obj = LoanGuarantor.objects.get(id=self.kwargs["loan_guarantor_id"])
        return loan_obj if loan_obj.guarantor_status == 'pending' else "decision-made"
    
    def get(self, request, *args, **kwargs):
   
        if self.get_object() == "decision-made":
            return Response({
                "success": "false",
                "message": "You have made your decision"
            }, status=status.HTTP_409_CONFLICT)
        return super().get(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        if self.get_object() == "decision-made":
            return Response({
                "success": "false",
                "message": "You have made your decision"
            }, status=status.HTTP_409_CONFLICT)
        return super().put(request, *args, **kwargs)
    

class AdminGetLoanRequestAPIView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RequestForLoanSerializer
    queryset = RequestForLoan.objects.all()

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    

class AdminApproveLoanRequestAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RequestForLoanSerializer

    def get_object(self):
        request_for_loan_obj = RequestForLoan.objects.get(id=self.kwargs["loan_id"])
        return request_for_loan_obj
    
    def put(self, request, *args, **kwargs):
        user = self.request.user

        if user:
            request_for_loan_obj = self.get_object()
            loan_status = request.data["loan_status"]
            request_for_loan_obj.loan_status = loan_status
            request_for_loan_obj.save()
            loan_request_decision_mail(
                request_for_loan_obj
            )

            return Response({
                    "success": "true",
                    "message": f"loan request {loan_status}"
                })
        
    