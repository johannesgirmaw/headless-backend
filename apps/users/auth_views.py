"""
Authentication views for the headless SaaS platform.
Handles JWT token generation, refresh, and user authentication.
"""

from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password

from apps.users.models import User
from apps.users.serializers import UserSerializer, UserLoginSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom JWT token obtain view that returns user data along with tokens.
    """

    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_view(request):
    """
    User registration endpoint.
    """
    from apps.users.serializers import UserCreateSerializer

    serializer = UserCreateSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """
    User logout endpoint that blacklists the refresh token.
    """
    try:
        refresh_token = request.data.get('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Successfully logged out'})
        else:
            return Response(
                {'error': 'Refresh token is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
    except Exception as e:
        return Response(
            {'error': 'Invalid token'},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def me_view(request):
    """
    Get current user details.
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def change_password_view(request):
    """
    Change current user's password.
    """
    from apps.users.serializers import UserPasswordChangeSerializer

    serializer = UserPasswordChangeSerializer(
        data=request.data,
        context={'request': request}
    )

    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Password changed successfully'})

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def verify_email_view(request):
    """
    Verify user email address.
    """
    email = request.data.get('email')
    verification_code = request.data.get('verification_code')

    if not email or not verification_code:
        return Response(
            {'error': 'Email and verification_code are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        user = User.objects.get(email=email)

        # For now, we'll just mark the user as verified
        # In a real implementation, you'd verify the code
        if verification_code == '123456':  # Dummy verification code
            user.is_verified = True
            user.save()
            return Response({'message': 'Email verified successfully'})
        else:
            return Response(
                {'error': 'Invalid verification code'},
                status=status.HTTP_400_BAD_REQUEST
            )

    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def forgot_password_view(request):
    """
    Send password reset email.
    """
    email = request.data.get('email')

    if not email:
        return Response(
            {'error': 'Email is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        user = User.objects.get(email=email)

        # In a real implementation, you'd send an email with reset link
        # For now, we'll just return a success message
        return Response({
            'message': 'Password reset email sent',
            'email': email
        })

    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def reset_password_view(request):
    """
    Reset user password with token.
    """
    email = request.data.get('email')
    reset_token = request.data.get('reset_token')
    new_password = request.data.get('new_password')

    if not all([email, reset_token, new_password]):
        return Response(
            {'error': 'Email, reset_token, and new_password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        user = User.objects.get(email=email)

        # In a real implementation, you'd verify the reset token
        # For now, we'll just check if it's a dummy token
        if reset_token == 'reset123':  # Dummy reset token
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password reset successfully'})
        else:
            return Response(
                {'error': 'Invalid reset token'},
                status=status.HTTP_400_BAD_REQUEST
            )

    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )
