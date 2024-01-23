from django.shortcuts import render
from rest_framework import generics, permissions, serializers
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from finance.accounts.models import OTP
from django.shortcuts import redirect, HttpResponseRedirect
from django.views import View

User = get_user_model()

from finance.accounts.api.v1.serializers import (
    SignUpSerializer, 
    VerifyAccountSerializer,
    IntialSignInSerializer,
    FinalSignInSerializer
)

class SignUpAPIView(generics.CreateAPIView):
    serializer_class = SignUpSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class VerifyAccountAPIView(generics.GenericAPIView):
    serializer_class = VerifyAccountSerializer
    permission_classes = [permissions.AllowAny]


    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.kwargs, context={"uid": kwargs["uidb64"], "token": kwargs["token"]})       
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
                return redirect("invalid_link") 
            
        return HttpResponseRedirect("https://finance-me-blond.vercel.app/auth")  

class IntialSignInAPIView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny,]
    serializer_class = IntialSignInSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data)

class FinalSignInAPIView(generics.GenericAPIView):
    """
        This is for 2FA
    """
    serializer_class = FinalSignInSerializer
    permission_classes = [permissions.AllowAny, ]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data)
    
class InvalidLinkView(View):
    template_name = 'accounts_activation/invalid_activation_link.html'

    def get(self, request):
        return render(request, self.template_name)
    
class SuccessPageView(View):
    template_name = 'accounts_activation/success_page.html'

    def get(self, request):
        return render(request, self.template_name)

