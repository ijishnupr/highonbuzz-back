from django.contrib import admin
from django.urls import path, include
from .views import *


urlpatterns = [
    path('register-client/', registration, name='register-client'),
    path('influencer-login/', influencer_login, name='influencer-login'),
    path('send-otp/', send_otp,),
    path('brand-register/', brand_registration, name='register'),
    path('brand-login/', brand_login, name='brand-login'),
    path('update-brand-profile/', update_brand_profile, name='update_brand_profile'),
    path('get-brand-profile/', get_brand_profile, name='get_brand_profile'),
    path('get-influencer-profile/', get_influencer_profile, name='get_influencer_profile'),
    #patch
    path('update-brand-profile-details/', update_brand_profile_details, name='update_brand_profile_details'),
    path('update-influencer-profile-details/', update_influencer_profile_details, name='update_influencer_profile_details'),



]