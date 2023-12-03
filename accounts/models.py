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
    profile_picture = models.ImageField(upload_to='brand_profiles/', null=True, blank=True)
    brand_description = models.TextField(null=True, blank=True)
    years_of_establishment = models.PositiveIntegerField(null=True, blank=True)
    number_of_products = models.PositiveIntegerField(null=True, blank=True)
    about_services = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.brand_name}'s Profile"



class InfluencerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='influencer_profile')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.IntegerField()
    location = models.CharField(max_length=255)
    instagram_profile = models.URLField(blank=True, null=True)
    instagram_earnings = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    youtube_profile = models.URLField(blank=True, null=True)
    youtube_earnings = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Influencer Profile"