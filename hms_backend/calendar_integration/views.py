from django.shortcuts import redirect
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .utils import get_auth_url, handle_oauth_callback
import requests

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def google_oauth_url(request):
    """Get Google OAuth authorization URL"""
    try:
        auth_url, state = get_auth_url()
        request.session['oauth_state'] = state
        return Response({'auth_url': auth_url}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def google_oauth_callback(request):
    """Handle Google OAuth callback"""
    code = request.GET.get('code')
    state = request.GET.get('state')
    
    if not code:
        return redirect('login')
    
    # Verify state
    if state != request.session.get('oauth_state'):
        return Response({'error': 'Invalid state parameter'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        tokens = handle_oauth_callback(code, state)
        
        # Save tokens to user
        user = request.user
        user.google_access_token = tokens['access_token']
        user.google_refresh_token = tokens.get('refresh_token')
        user.save()
        
        return Response({'message': 'Google Calendar connected successfully'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_google_connection(request):
    """Check if user has Google Calendar connected"""
    user = request.user
    is_connected = bool(user.google_access_token)
    return Response({'is_connected': is_connected}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def disconnect_google(request):
    """Disconnect Google Calendar"""
    user = request.user
    user.google_access_token = None
    user.google_refresh_token = None
    user.save()
    return Response({'message': 'Google Calendar disconnected'}, status=status.HTTP_200_OK)
