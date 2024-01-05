from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
import uuid


def user_images_upload_location(instance, file_name):
    return f"users/images/{file_name}"


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=150, blank=False, null=False)
    last_name = models.CharField(max_length=150, blank=False, null=False)
    email = models.EmailField(blank=False, null=False, unique=True)
    nin = models.CharField(max_length=40, blank=False,null=False, unique=True)
    phone_number = models.CharField(max_length=20, blank=False, null=False, unique=True)
    gender = models.CharField(max_length=10, blank=False, null=False)
    bank_name = models.CharField(max_length=40, blank=False, null=False)
    bank_account_number = models.CharField(max_length=40, blank=False, null=False, unique=True)
    date_of_birth = models.DateTimeField(blank=False, null=False)
    image = models.ImageField(upload_to=user_images_upload_location, blank=False, null=False)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class OTP(models.Model):
    otp = models.CharField(max_length=10, blank=False, null=False)
    email = models.EmailField(max_length=60, blank=False, null=False, unique=True)
    time_created = models.DateTimeField(auto_now=True)
