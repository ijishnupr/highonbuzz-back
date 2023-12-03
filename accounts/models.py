from django.db import models

# Create your models here.
from django.db import models
from django.db import models
from django.core.validators import RegexValidator
from .validators import *
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, role='user', registered_by=None, profile_img=None, mobile=None,
                    **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, role=role, registered_by=registered_by, profile_img=profile_img, mobile=mobile,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, role='admin', registered_by=None, profile_img=None, mobile=None,
                         **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, role, registered_by, profile_img, mobile, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLES = [
        ('admin', 'Admin'),
        ('influencer', 'Influencer'),
        ('brand', 'Brand'),
    ]

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLES, default='user', validators=[CheckIfAlpha, CheckNull])
    registered_by = models.CharField(max_length=255, blank=True, null=True, validators=[CheckIfAlpha, CheckNull])
    profile_img = models.ImageField(upload_to='profile_images/', blank=True, null=True, validators=[CheckNull])
    mobile = models.CharField(max_length=15, blank=True, null=True, validators=[phone_regex])

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role']

    def __str__(self):
        return self.email


class MobileOTP(models.Model):
    otp = models.CharField(max_length=6)
    time = models.DateTimeField(auto_now=True)  # Updated when the OTP is filled
    mobile = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.mobile} - {self.otp}"



class BrandProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='brand_profile')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    brand_name = models.CharField(max_length=255)
    business_name_url = models.URLField()

    def __str__(self):
        return f"{self.brand_name}'s Profile"