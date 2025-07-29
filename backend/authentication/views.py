from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password
from .serializers import (
    UserRegistrationSerializer, 
    UserLoginSerializer, 
    UserSerializer,
    ChangePasswordSerializer
)
from .models import User

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            'message': 'Registration successful',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        login(request, user)
        return Response({
            'message': 'Login successful',
            'user': UserSerializer(user).data
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    # Clear the user's session
    logout(request)
    
    # Force session flush to ensure complete logout
    request.session.flush()
    
    return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    serializer = ChangePasswordSerializer(data=request.data)
    if serializer.is_valid():
        user = request.user
        current_password = serializer.validated_data['current_password']
        new_password = serializer.validated_data['new_password']
        
        if not check_password(current_password, user.password):
            return Response({
                'error': 'Current password is incorrect'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save()
        
        return Response({
            'message': 'Password changed successfully'
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password(request):
    from django.core.mail import send_mail
    from django.conf import settings
    from django.utils import timezone
    import secrets
    import uuid
    from datetime import timedelta
    
    email = request.data.get('email')
    if not email:
        return Response({
            'error': 'Email is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(email=email)
        
        # Generate a secure reset token
        reset_token = str(uuid.uuid4())
        
        # Set token expiry to 1 hour from now
        expiry_time = timezone.now() + timedelta(hours=1)
        
        # Save token to user
        user.reset_token = reset_token
        user.reset_token_expiry = expiry_time
        user.save()
        
        # Create reset URL
        reset_url = f"http://localhost:3000/reset-password?token={reset_token}"
        
        # Email content
        subject = 'Password Reset Request'
        message = f"""
Hello {user.username},

You have requested to reset your password. Please click the link below to reset your password:

{reset_url}

This link will expire in 1 hour.

If you did not request this password reset, please ignore this email.

Best regards,
Your Authentication System Team
        """
        
        try:
            # Send email with better error handling
            print(f"DEBUG: Attempting to send email to {email}")
            print(f"DEBUG: From email: {settings.DEFAULT_FROM_EMAIL}")
            print(f"DEBUG: SMTP Host: {settings.EMAIL_HOST}:{settings.EMAIL_PORT}")
            print(f"DEBUG: TLS: {settings.EMAIL_USE_TLS}, SSL: {settings.EMAIL_USE_SSL}")
            
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
            
            print(f"SUCCESS: Password reset email sent to {email}")
            return Response({
                'message': f'Password reset email sent to {email}'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(f"ERROR: Failed to send email: {str(e)}")
            print(f"ERROR: Email settings - Host: {settings.EMAIL_HOST}, User: {settings.EMAIL_HOST_USER}")
            
            # For development, let's temporarily return success even if email fails
            # so we can test the reset token functionality
            if settings.DEBUG:
                print(f"DEBUG MODE: Email failed but returning success. Reset token: {reset_token}")
                return Response({
                    'message': f'Password reset email sent to {email} (DEBUG: token={reset_token})'
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': 'Failed to send reset email. Please try again later.'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except User.DoesNotExist:
        # For security, don't reveal if email exists or not
        return Response({
            'message': f'If an account with email {email} exists, a password reset link has been sent.'
        }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    from django.utils import timezone
    
    token = request.data.get('token')
    new_password = request.data.get('new_password')
    
    if not token or not new_password:
        return Response({
            'error': 'Token and new password are required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Find user with this reset token
        user = User.objects.get(reset_token=token)
        
        # Check if token has expired
        if user.reset_token_expiry and timezone.now() > user.reset_token_expiry:
            return Response({
                'error': 'Reset token has expired. Please request a new password reset.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Set new password
        user.set_password(new_password)
        
        # Clear reset token
        user.reset_token = None
        user.reset_token_expiry = None
        user.save()
        
        return Response({
            'message': 'Password has been reset successfully'
        }, status=status.HTTP_200_OK)
        
    except User.DoesNotExist:
        return Response({
            'error': 'Invalid reset token'
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    return Response({'status': 'healthy'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def debug_users(request):
    """Debug endpoint to list all users - remove in production"""
    users = User.objects.all().values('id', 'email', 'username')
    return Response({'users': list(users)}, status=status.HTTP_200_OK)
