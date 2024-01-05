from rest_framework import serializers
from finance.loans.models import (
    RequestableLoanAmount, 
    RequestForLoan,
    LoanGuarantor
)
from django.contrib.auth import get_user_model
from django.db import transaction
from finance.loans.mails import request_for_guarantorship_mail
User = get_user_model()


class RequestableLoanAmountSerializer(serializers.ModelSerializer):

    class Meta:
        model = RequestableLoanAmount
        fields = [
            'id',
            'amount'
        ]


    def validate(self, attrs):
        amount = RequestableLoanAmount.objects.filter(amount=attrs["amount"])

        if amount.exists():
            raise serializers.ValidationError({
                "error": "true",
                "message": f"amount {attrs["amount"]} exists"
            })

        # if self.context['request'].method == 'POST':
        #  user_id = self.context["request"].user.id
        #  is_user_staff_or_admin = User.objects.filter(
        #     Q(id=user_id, is_staff=True) | Q(id=user_id, is_admin=True)
        #     ).first()
        #  if is_user_staff_or_admin:
        #      return attrs
        #  else:
        #      raise serializers.ValidationError({
        #         "error": "true",
        #         "message": "User not authorized"
        #     })
        return attrs
    

    def create(self, validated_data):
        
        loan_amount = RequestableLoanAmount.objects.create(
            **validated_data
        )
        return loan_amount
    
class GuarantorSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(write_only=True)
    
    class Meta:
        model = LoanGuarantor
        fields = [
            'email',
            'guarantor_first_name',
            'guarantor_last_name',
            'phone_number',
            'home_address',
            'image',
            'guarantor_status',
            'occupation',
            'home_address'
        ]

    def validate(self, attrs):
        
        user = User.objects.get(id=self.context["request"].user.id)
        if user.phone_number == attrs["phone_number"]:
            raise serializers.ValidationError({
                "message": "you can't use your phone number as a guarantor nin"
            })
        if user.email == attrs["email"]:
            raise serializers.ValidationError({
                "message": "you can't use your email as a guarantor email"
            })

        return attrs




class RequestForLoanSerializer(serializers.ModelSerializer):
    guarantors = serializers.ListSerializer(
        child=GuarantorSerializer(), required=True
    )
    class Meta:
        model = RequestForLoan
        fields = [
            'id',
            'guarantors',
            'amount',
            'loan_status'
        ]

    
    def validate(self, attrs):
        requestable_amount_objs = RequestableLoanAmount.objects.all()
        requestable_amounts = [requestable_amount_obj.amount for requestable_amount_obj in requestable_amount_objs ]
        
        if attrs["amount"] not in requestable_amounts:
            raise serializers.ValidationError({
                "message": f"Choose the requestable amount"
            })

        return attrs


    @transaction.atomic
    def create(self, validated_data):            

        request_for_loan_obj =  RequestForLoan.objects.create(
            user=self.context["request"].user,
            amount=validated_data["amount"]
        )
        guarantors = validated_data.pop('guarantors')
        
        with transaction.atomic():
            for guarantor in guarantors:
               loan_guarantor = LoanGuarantor.objects.create(
                    request_for_loan=request_for_loan_obj,
                    **guarantor
                    )
               request_for_guarantorship_mail(
                    self.context["request"].user,
                    loan_guarantor,
                    request_for_loan_obj.id,
                    validated_data["amount"],
                    )
                
            
        return request_for_loan_obj
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data


class GuarantorDecisonSerializer(serializers.ModelSerializer):
    # image = serializers.ImageField(required=True)
    guarantor_nin = serializers.CharField(required=True, write_only=True)
    earning_per_month = serializers.CharField(required=True)
    occupation = serializers.CharField(required=True)
    guarantor_status = serializers.CharField(required=True)
    class Meta:
        model = LoanGuarantor
        fields = [
            'guarantor_first_name',
            'guarantor_last_name',
            # 'image',
            'guarantor_nin',
            'earning_per_month',
            'occupation',
            'guarantor_status'
        ]


    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    
    def to_representation(self, instance):
        if self.context['request'].method == 'GET':
            data = super().to_representation(instance)
            request_for_loan_info = LoanGuarantor.objects.get(id=instance.id).request_for_loan
            data["amount"] =  request_for_loan_info.amount      
            data["requestor_name"] = f"{request_for_loan_info.user.first_name} {request_for_loan_info.user.last_name}"
            return data
        return super().to_representation(instance)


class AdminApproveLoanSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = RequestForLoan
        fields = [
            'guarantors',
            'loan_status',
            'amount',
        ]

    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)