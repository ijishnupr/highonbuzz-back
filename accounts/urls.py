from django.contrib import admin
from django.urls import path, include
from .views import *


urlpatterns = [
    path('register-client/', registration, name='register-client'),
    path('influencer-login/', influencer_login, name='influencer-login'),
    path('send-otp/', send_otp,),
    path('brand-register/', brand_registration, name='register'),
    path('brand-login/', brand_login, name='brand-login')



]