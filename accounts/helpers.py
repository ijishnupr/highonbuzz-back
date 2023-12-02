import requests
import random
from django.conf import settings



def send_otp_to_phone(mobile):
    try:
        otp = random.randint(1000, 9999)
        url = f'https://2factor.in/API/V1/{settings.API_KEY}/SMS/{mobile}/{otp}'
        response = requests.get(url)
        return otp

    except Exception as e:
        return None