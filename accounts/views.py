from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny , IsAuthenticated
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


# @api_view(['POST'])
# @permission_classes([AllowAny])
# def registration(request):
#     if request.method == 'POST':
#         serializer = RegisterClientSerializer(data=request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data['email']
#             mobile = serializer.validated_data['mobile']
#             password = serializer.validated_data['password']
#             provided_otp = serializer.validated_data['otp']

#             # Check if the email is unique
#             if User.objects.filter(email=email).exists():
#                 return Response({'detail': 'This email is already registered.'}, status=status.HTTP_400_BAD_REQUEST)

#             # Check if the mobile is unique
#             if User.objects.filter(mobile=mobile).exists():
#                 return Response({'detail': 'This mobile number is already registered.'},
#                                 status=status.HTTP_400_BAD_REQUEST)

#             # Check if the provided OTP matches the latest OTP in MobileOTP
#             latest_otp = MobileOTP.objects.filter(mobile=mobile).order_by('-time').first()

#             if latest_otp is None or provided_otp != latest_otp.otp:
#                 return Response({'detail': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)

#             # Create and save the new user
#             serializer.save()

#             return Response(serializer.data, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     return Response({'detail': 'Invalid request method.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



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
            user = serializer.save()

            # Extract additional fields for InfluencerProfile
            first_name = request.data.get('firstname', '')  # Change to 'firstname'
            last_name = request.data.get('lastname', '')  # Change to 'lastname'
            age = request.data.get('age', '')
            location = request.data.get('location', '')

            # Create an InfluencerProfile instance
            influencer_profile = InfluencerProfile.objects.create(
                user=user,
                first_name=first_name,
                last_name=last_name,
                age=age,
                location=location,
                # You can add other fields as needed
            )

            return Response({'detail': 'Successfully registered influencer'}, status=status.HTTP_201_CREATED)

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


# @api_view(['POST'])
# @permission_classes([AllowAny])
# def brand_registration(request):
#     if request.method == 'POST':
#         serializer = RegisterBrandSerializer(data=request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data['email']
#             mobile = serializer.validated_data['mobile']
#             password = serializer.validated_data['password']
#             provided_otp = serializer.validated_data['otp']

#             # Check if the email is unique
#             if User.objects.filter(email=email).exists():
#                 return Response({'detail': 'This email is already registered.'}, status=status.HTTP_400_BAD_REQUEST)

#             # Check if the mobile is unique
#             if User.objects.filter(mobile=mobile).exists():
#                 return Response({'detail': 'This mobile number is already registered.'},
#                                 status=status.HTTP_400_BAD_REQUEST)

#             # Check if the provided OTP matches the latest OTP in MobileOTP
#             latest_otp = MobileOTP.objects.filter(mobile=mobile).order_by('-time').first()

#             if latest_otp is None or provided_otp != latest_otp.otp:
#                 return Response({'detail': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)

#             # Create and save the new brand user
#             user = serializer.save()

#             # Create a BrandProfile instance
#             brand_profile = BrandProfile.objects.create(
#                 user=user,
#                 # You can add other fields as needed
#             )

#             return Response({'detail': 'Successfully registered brand'}, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     return Response({'detail': 'Invalid request method.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# views.py

@api_view(['POST'])
@permission_classes([AllowAny])
def brand_registration(request):
    if request.method == 'POST':
        serializer = RegisterBrandSerializer(data=request.data)
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

            # Create and save the new brand user
            user = serializer.save()

            # Extract additional fields for BrandProfile
            first_name = request.data.get('firstname', '')  # Change to 'firstname'
            last_name = request.data.get('lastname', '')  # Change to 'lastname'
            brand_name = request.data.get('brand_name', '')
            business_name_url = request.data.get('business_name_url', '')

            # Create a BrandProfile instance
            brand_profile = BrandProfile.objects.create(
                user=user,
                first_name=first_name,
                last_name=last_name,
                brand_name=brand_name,
                business_name_url=business_name_url,
                # You can add other fields as needed
            )

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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_brand_profile(request):
    user = request.user
    brand_profile = user.brand_profile  # Assuming you have a one-to-one relationship between User and BrandProfile

    if request.method == 'POST':
        serializer = BrandProfileSerializer(brand_profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'Brand profile updated successfully'}, status=200)
        return Response(serializer.errors, status=400)

    return Response({'detail': 'Invalid request method.'}, status=405)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_brand_profile(request):
    user = request.user
    try:
        brand_profile = BrandProfile.objects.get(user=user)
    except BrandProfile.DoesNotExist:
        return Response({'detail': 'Brand profile not found.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = BrandProfileSerializer(brand_profile)
    
    data = {
        'user': {
            'email': user.email,
            'mobile': user.mobile,
            # Add other user-related fields
        },
        'brand_profile': serializer.data
    }

    return Response(data, status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_influencer_profile(request):
    user = request.user
    try:
        influencer_profile = InfluencerProfile.objects.get(user=user)
    except InfluencerProfile.DoesNotExist:
        return Response({'detail': 'Influencer profile not found.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = InfluencerProfileSerializer(influencer_profile)
    
    data = {
        'user': {
            'email': user.email,
            'mobile': user.mobile,
            # Add other user-related fields
        },
        'influencer_profile': serializer.data
    }

    return Response(data, status=status.HTTP_200_OK)



@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_brand_profile_details(request):
    user = request.user

    try:
        brand_profile = BrandProfile.objects.get(user=user)
    except BrandProfile.DoesNotExist:
        return Response({'detail': 'Brand profile not found.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = BrandProfileSerializer(brand_profile, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({'detail': 'Brand profile details updated successfully'}, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_influencer_profile_details(request):
    user = request.user

    try:
        influencer_profile = InfluencerProfile.objects.get(user=user)
    except InfluencerProfile.DoesNotExist:
        return Response({'detail': 'Influencer profile not found.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = InfluencerProfileSerializer(influencer_profile, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({'detail': 'Influencer profile details updated successfully'}, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)