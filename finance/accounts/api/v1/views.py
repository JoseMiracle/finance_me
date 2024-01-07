from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from finance.accounts.models import OTP


User = get_user_model()

from finance.accounts.api.v1.serializers import (
    SignUpSerializer, 
    VerifyOtpAPISerializer,
    IntialSignInSerializer,
    FinalSignInSerializer
)

class SignUpAPIView(generics.CreateAPIView):
    serializer_class = SignUpSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class VerifyOtpAPIView(generics.GenericAPIView):
    serializer_class = VerifyOtpAPISerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(email=serializer.validated_data["email"])
        user.is_active = True
        user.save()
        OTP.objects.get(otp=serializer.validated_data["otp"],
                        user=user
                        ).delete()
        return Response({
            "message": "account activated"
        })



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
    
