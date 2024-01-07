from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db import transaction
from finance.accounts.models import OTP
from finance.accounts.mails import account_activation_mail, sign_in_with_otp_activation_mail
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
        full_name = f"{user.first_name} {user.last_name}"
        account_activation_mail(user.email, generated_otp, full_name)
        OTP.objects.create(
            otp=generated_otp,
            user=user
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
            user=user
            ).first()
    
        period_of_user_otp = (timezone.now() - user_otp.time_created).total_seconds()
        
        if user is None:
            raise serializers.ValidationError({
                "error": "true",
                "message": "user doesn't exist"
            })
        
        if (user and user_otp is None):
            raise serializers.ValidationError({
                "error": "true",
                "message": "OTP doesn't exist" 
            })
        
        if (user and period_of_user_otp > constansts.OTP_TIMEOUT):
             user_otp.delete()
             raise serializers.ValidationError({
                "error": "true",
                "message": "OTP expired" 
            })
        

        if (user and period_of_user_otp <= constansts.OTP_TIMEOUT):
           return attrs
       



class IntialSignInSerializer(serializers.Serializer):
    email_or_username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, attrs):
        user = User.objects.filter(
            Q(email=attrs["email_or_username"]) | Q(username=attrs["email_or_username"])
            ).first()
        generated_otp = generate_otp()
        full_name = f"{user.first_name} {user.last_name}"
        
        if user is None or user.is_active == False:
            raise serializers.ValidationError({
                "error": "true",
                "messsage": "user doesn't exist or inactive account"
            })
        
        if user and (user.check_password(attrs["password"]) == False):
            raise serializers.ValidationError({
                "error": "true",
                "messsage": "Invalid Password"
            })

        if user and user.check_password(attrs["password"]):
            sign_in_with_otp_activation_mail(
                user.email,
                full_name,
                generated_otp,
            )
            
            obj, created = OTP.objects.get_or_create(
               user=user,
                defaults={
                    'otp': generated_otp
                }
            )
            if obj:
                obj.otp = generated_otp
                obj.time_created = timezone.now()
                obj.save()
            attrs["username"] = user.username
            return attrs
    
    def to_representation(self, attrs):
        attrs.pop('password')
        attrs["error"] = "false"
        return attrs
    
class FinalSignInSerializer(serializers.Serializer):
    email_or_username = serializers.CharField()
    otp = serializers.CharField(min_length=6)

    def validate(self, attrs):
        user = User.objects.filter(
            Q(email=attrs["email_or_username"]) | Q(username=attrs["email_or_username"])
            ).first()
        user_otp = OTP.objects.filter(user=user, 
                                       otp=attrs["otp"]).first()     
        if (user is None):
            raise serializers.ValidationError(
                {
                    "error": "true",
                    "message": "user doesn't exist"
                }
            )

        if(user and user_otp):
            user_otp = OTP.objects.filter(user=user, 
                                       otp=attrs["otp"]).first()
            period_of_user_otp = (timezone.now() - user_otp.time_created).total_seconds()
            
            if (period_of_user_otp >= constansts.OTP_TIMEOUT) :
                raise serializers.ValidationError({
                    "error": "true",
                    "message": "invalid otp or token expired " 
                })        
            
            if(period_of_user_otp < constansts.OTP_TIMEOUT):
                OTP.objects.get(
                    user=user, 
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




            
            
