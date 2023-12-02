from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import *
from django.contrib.auth import authenticate
from .helpers import *
from .models import *


@api_view(['POST'])
def send_otp(request):
    data = request.data

    if data.get('mobile') is None:
        return Response({
            'status': 400,
            'message': 'mobile key is required'
        })

    try:
        mobile = data.get('mobile')
        otp = send_otp_to_phone(mobile)

        # Print the generated OTP in the console
        print(f"Generated OTP for mobile {mobile}: {otp}")

        # Create a MobileOTP instance
        mobile_otp = MobileOTP.objects.create(
            mobile=mobile,
            otp=otp
        )

        return Response({
            'status': 200,
            'message': 'OTP SENT'
        })

    except Exception as e:
        return Response({
            'status': 500,
            'message': f'Error: {str(e)}'
        })


@api_view(['POST'])
@permission_classes([AllowAny])
def registration(request):
    if request.method == 'POST':
        serializer = RegisterClientSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            mobile = serializer.validated_data['mobile']
            password = serializer.validated_data['password']
            provided_otp = serializer.validated_data['otp']

            # Check if the email is unique
            if User.objects.filter(email=email).exists():
                return Response({'detail': 'This email is already registered.'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the mobile is unique
            if User.objects.filter(mobile=mobile).exists():
                return Response({'detail': 'This mobile number is already registered.'},
                                status=status.HTTP_400_BAD_REQUEST)

            # Check if the provided OTP matches the latest OTP in MobileOTP
            latest_otp = MobileOTP.objects.filter(mobile=mobile).order_by('-time').first()

            if latest_otp is None or provided_otp != latest_otp.otp:
                return Response({'detail': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)

            # Create and save the new user
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({'detail': 'Invalid request method.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
@permission_classes([AllowAny])
def influencer_login(request):
    if request.method == 'POST':
        serializer = InfluencerLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = authenticate(request, email=email, password=password)

            if user is not None:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'detail': 'Successfully logged in', 'token': token.key}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({'detail': 'Invalid request method.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
@permission_classes([AllowAny])
def brand_registration(request):
    if request.method == 'POST':
        serializer = RegisterBrandSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'Successfully registered brand'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({'detail': 'Invalid request method.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
@permission_classes([AllowAny])
def brand_login(request):
    if request.method == 'POST':
        serializer = BrandLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, username=email, password=password)

            if user is not None:
                # Authentication successful, create or get the token
                token, created = Token.objects.get_or_create(user=user)
                return Response({'detail': 'Successfully logged in', 'token': token.key}, status=status.HTTP_200_OK)

            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({'detail': 'Invalid request method.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)