# serializers.py

from rest_framework import serializers
from .models import *
from .validators import phone_regex


class RegisterClientSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    otp = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'mobile', 'password', 'otp']

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            mobile=validated_data['mobile'],
            role='influencer',  # Set the role to 'influencer'
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


# class RegisterBrandSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)

#     class Meta:
#         model = User
#         fields = ['email', 'password']

#     def create(self, validated_data):
#         user = User.objects.create(
#             email=validated_data['email'],
#             role='brand',  # Set the role to 'brand'
#         )
#         user.set_password(validated_data['password'])
#         user.save()
#         return user

class RegisterBrandSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    otp = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'otp', 'mobile']  # Include 'mobile' in the fields

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            mobile=validated_data['mobile'],
            role='brand',  # Set the role to 'brand'
        )
        user.set_password(validated_data['password'])
        user.save()
        
        return user


class InfluencerLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})


class BrandLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})




class BrandProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandProfile
        fields = ['first_name', 'last_name', 'brand_name', 'business_name_url']