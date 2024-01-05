from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db import transaction
from finance.accounts.models import OTP
from finance.accounts.mails import otp_for_account_activation, otp_for_sign_in
from finance.accounts.utils import generate_otp
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q
from django.utils import timezone
from finance.accounts import constansts

User = get_user_model()



class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    image = serializers.ImageField(required=True, allow_empty_file=False)
    nin  = serializers.CharField(min_length=10, write_only=True)
    bank_account_number = serializers.CharField(min_length=10)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'nin',
            'phone_number',
            'gender',
            'bank_name',
            'bank_account_number',
            'date_of_birth',
            'password',
            'username',
            'image'
        ]

    def validate(self, attrs):
        return super().validate(attrs)

    @transaction.atomic
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.is_active = False
        user.save()

        generated_otp = generate_otp()
        
        otp_for_account_activation(user.email, generated_otp)
        OTP.objects.create(
            otp=generated_otp, 
            email=validated_data["email"]
            )
        return user
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'image'
        ]
        
    


class VerifyOtpAPISerializer(serializers.Serializer):
    otp = serializers.CharField(min_length=6, max_length=6)
    email = serializers.EmailField()

    def validate(self, attrs):
        user  = User.objects.filter(email=attrs["email"]).first()

        user_otp = OTP.objects.filter(
            otp=attrs["otp"],
            email=attrs["email"]
            )
        
        if user is None:
            raise serializers.ValidationError({
                "error": "true",
                "message": "user doesn't exist"
            })
        
        if user and (user_otp.first() is None):
            raise serializers.ValidationError({
                "error": "true",
                "message": "Otp invalid or doesn't exist" 
            })
        
        if user and user_otp.exists():
           return attrs
       



class IntialSignInSerializer(serializers.Serializer):
    email_or_username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, attrs):
        user = User.objects.filter(
            Q(email=attrs["email_or_username"]) | Q(username=attrs["email_or_username"])
            ).first()
        
        if user is None or user.is_active == False:
            raise serializers.ValidationError({
                "error": "true",
                "messsage": "user doesn't exist or inactive account"
            })
        
        if user and (user.check_password(attrs["password"]) == False):
            raise serializers.ValidationError({
                "error": "true",
                "messsage": "Pls recheck credentials"
            })

        if user and user.check_password(attrs["password"]):
            generated_otp = generate_otp()
            otp_for_sign_in(
                user.email,
                user.username,
                generated_otp,
            )
            user_otp = OTP.objects.filter(email=user.email).first()
            
            if user_otp is not None:
                user_otp.delete()
            
            OTP.objects.create(
                email=user.email,
                otp=generated_otp
            )
            attrs["username"] = user.username
            return attrs
    
    def to_representation(self, attrs):
        attrs.pop('password')
        attrs["error"] = "false"
        return attrs
    
class FinalSignInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(min_length=6)

    def validate(self, attrs):
        user = User.objects.filter(email=attrs['email']).first()

        user_otp = OTP.objects.filter(email=attrs["email"], 
                                       otp=attrs["otp"]).first()     
        if (user is None):
            raise serializers.ValidationError(
                {
                    "error": "true",
                    "message": "user doesn't exist"
                }
            )

        if(user and user_otp):
            period_of_user_otp = (timezone.now() - user_otp.time_created).total_seconds()
            
            if (period_of_user_otp > constansts.OTP_TIMEOUT) :
                raise serializers.ValidationError({
                    "error": "true",
                    "message": "invalid otp or token expired " 
                })        
            
            if(period_of_user_otp < constansts.OTP_TIMEOUT):
                OTP.objects.get(
                    email=attrs["email"], 
                    otp=attrs["otp"]).delete()
                return user
        
        if (user and user_otp is None):
             """
                user exists and token expired
             """
             raise serializers.ValidationError({
                    "error": "true",
                    "message": "invalid otp or token expired" 
                })
          
    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            "Info": f"Welcome {instance.username}", 
            "access_token": str(refresh.access_token),
            "user": UserSerializer(instance).data
            }




            
            
