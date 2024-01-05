from django.db import models
import uuid
from django.contrib.auth import get_user_model

User = get_user_model()


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class RequestableLoanAmount(BaseModel):
    amount = models.IntegerField()
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.amount}"
    


class RequestForLoan(BaseModel):
    REQUESTFORLOAN_STATUS = [
        ('pending', 'pending'),
        ('terminated', 'terminated'),
        ('rejected', 'rejected'),
        ('approved', 'approved'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    loan_status = models.CharField(max_length=40, choices=REQUESTFORLOAN_STATUS, default='pending')
    
    def __str__(self):
        return f"{self.user} request for {self.amount}"

class LoanGuarantor(BaseModel):
    GUARANTOR_CHOICES = [
        ('pending', 'pending'),
        ('accept', 'accept'),
        ('reject', 'reject')
    ]
    request_for_loan = models.ForeignKey(RequestForLoan, on_delete=models.CASCADE, related_name="guarantors")
    email = models.EmailField(blank=False, null=False)
    guarantor_first_name = models.CharField(max_length=100, blank=True, null=True)
    guarantor_last_name = models.CharField(max_length=100, blank=True, null=True)
    guarantor_nin = models.CharField(max_length=40)
    phone_number = models.CharField(max_length=20, null=False)
    home_address = models.CharField(max_length=100, blank=False, null=False)
    guarantor_status = models.CharField(max_length=20, choices=GUARANTOR_CHOICES, default='pending')
    occupation = models.CharField(max_length=100)
    earning_per_month = models.CharField(max_length=100)
    image = models.ImageField()
    
    def __str__(self) -> str:
        return f"{self.guarantor_first_name} {self.guarantor_last_name} for {self.request_for_loan.user} loan"


class LoansApprovedByStaff(BaseModel):
    user = models.ForeignKey(User,on_delete=models.PROTECT)
    loan_approved = models.ForeignKey(RequestForLoan, on_delete=models.PROTECT)






 

