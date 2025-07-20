import imghdr
import base64
import sys
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from .serializers import UserSerializer, RegisterSerializer
from .models import User


# Create your views here.
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({"detail": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, username=username, password=password)

    if user is not None:
        if not user.IsActive:
            return Response({"detail": "Account is deactivated."}, status=status.HTTP_403_FORBIDDEN)
        
        # Create or get token for the user
        token, created = Token.objects.get_or_create(user=user)
        
        # Also maintain session for backward compatibility
        login(request, user)
        
        return Response({
            "message": "Login successful",
            "token": token.key,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role,
                "isVerified": user.isVerified,
                "IsActive": user.IsActive
            }
        }, status=status.HTTP_200_OK)

    return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        # Delete the user's token to logout
        request.user.auth_token.delete()
    except Token.DoesNotExist:
        pass
    
    logout(request)
    return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def register(request):
    # Return all users that are registered
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response({'users': serializer.data})
    
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Create token for the new user
            token, created = Token.objects.get_or_create(user=user)
            
            # Also login for session
            login(request, user)
            
            return Response({
                "message": "Registration successful",
                "token": token.key,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "role": user.role,
                    "isVerified": user.isVerified,
                    "IsActive": user.IsActive
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def activate_account(request):
    user = request.user
    user.isVerified = True
    user.save()
    return Response({'detail': 'Account activated.'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_profile_image(request):
    try:
        image = request.data.get('profileImage')
        if not image:
            return Response({'detail': 'No image provided.'}, status=status.HTTP_400_BAD_REQUEST)

        if image.startswith('data:image/'):
            header, data = image.split(';base64,')
            file_ext = header.split('/')[-1]
            allowed_types = ['jpeg', 'jpg', 'png']
            if file_ext not in allowed_types:
                return Response({'detail': 'Invalid image type. Only jpg, jpeg, png allowed.'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                decoded_file = base64.b64decode(data)
            except Exception:
                return Response({'detail': 'Invalid image data.'}, status=status.HTTP_400_BAD_REQUEST)
            if len(decoded_file) > 2 * 1024 * 1024:
                return Response({'detail': 'Image size exceeds 2MB.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            allowed_types = ['jpeg', 'jpg', 'png']
            if not any(image.lower().endswith('.' + ext) for ext in allowed_types):
                return Response({'detail': 'Invalid image type. Only jpg, jpeg, png allowed.'}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        user.profileImage = image
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data)
    except Exception as e:
        return Response({'detail': 'Invalid image data.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    try:
        user = request.user
        data = request.data
        
        # Update basic fields
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'email' in data:
            # Check if email is already taken by another user
            if User.objects.exclude(id=user.id).filter(email=data['email']).exists():
                return Response({'detail': 'Email already in use.'}, status=status.HTTP_400_BAD_REQUEST)
            user.email = data['email']
        if 'phoneNumber' in data:
            # Check if phone number is already taken by another user
            if data['phoneNumber'] and User.objects.exclude(id=user.id).filter(phoneNumber=data['phoneNumber']).exists():
                return Response({'detail': 'Phone number already in use.'}, status=status.HTTP_400_BAD_REQUEST)
            user.phoneNumber = data['phoneNumber']
        if 'address' in data:
            user.address = data['address']
        
        # Update seller-specific fields if user is a seller
        if user.role == 'seller':
            if 'storeName' in data:
                # Check if store name is already taken by another user
                if data['storeName'] and User.objects.exclude(id=user.id).filter(storeName=data['storeName']).exists():
                    return Response({'detail': 'Store name already in use.'}, status=status.HTTP_400_BAD_REQUEST)
                user.storeName = data['storeName']
            if 'storeDescription' in data:
                user.storeDescription = data['storeDescription']
        
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data)
        
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deactivate_account(request):
    user = request.user
    user.IsActive = False
    user.save()
    logout(request)
    return Response({'detail': 'Account deactivated.'})

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def admin_change_password(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
    password = request.data.get('password')
    if not password:
        return Response({'detail': 'No password provided.'}, status=status.HTTP_400_BAD_REQUEST)
    user.set_password(password)
    user.save()
    return Response({'detail': 'Password changed.'})

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def admin_create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.role = 'admin'
        user.is_staff = True
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def admin_get_user(request, user_id):
    try:
        user = User.objects.get(pk=user_id, role='admin')
    except User.DoesNotExist:
        return Response({'detail': 'Admin user not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = UserSerializer(user)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def admin_delete_user(request, user_id):
    try:
        user = User.objects.get(pk=user_id, role='admin')
    except User.DoesNotExist:
        return Response({'detail': 'Admin user not found.'}, status=status.HTTP_404_NOT_FOUND)
    user.delete()
    return Response({'detail': 'Admin user deleted.'})

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated, IsAdminUser])
def admin_update_user(request, user_id):
    try:
        user = User.objects.get(pk=user_id, role='admin')
    except User.DoesNotExist:
        return Response({'detail': 'Admin user not found.'}, status=status.HTTP_404_NOT_FOUND)
    partial = request.method == 'PATCH'
    serializer = UserSerializer(user, data=request.data, partial=partial)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)