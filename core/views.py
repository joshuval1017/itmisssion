from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from .forms import CitizenSignupForm

User = get_user_model()

# 🌐 Landing Page
def landing_page(request):
    return render(request, 'landing.html', {'year': datetime.now().year})


# 📝 Signup View
def signup_view(request):
    if request.method == 'POST':
        form = CitizenSignupForm(request.POST)
        if form.is_valid():
            citizen = form.save(commit=False)
            citizen.set_password(form.cleaned_data['password'])
            citizen.save()
            return redirect('landing')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CitizenSignupForm()
    return render(request, 'signup.html', {'form': form})


# 🔐 Login View (JWT + Email-based)
class LoginView(APIView):
    def get(self, request):
        return Response({'detail': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)

        user = authenticate(request, username=user_obj.username, password=password)
        if user is None:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        response = Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        response.set_cookie('access', access_token, httponly=True, secure=True, samesite='Lax')
        response.set_cookie('refresh', refresh_token, httponly=True, secure=True, samesite='Lax')
        return response


# 🔄 Refresh Token View
class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh')
        if not refresh_token:
            return Response({'error': 'No refresh token'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            token = RefreshToken(refresh_token)
            new_access = str(token.access_token)
            new_refresh = str(token)  # Rotated refresh
            response = Response({'message': 'Token refreshed'}, status=status.HTTP_200_OK)
            response.set_cookie('access', new_access, httponly=True, secure=True, samesite='Lax')
            response.set_cookie('refresh', new_refresh, httponly=True, secure=True, samesite='Lax')
            return response
        except Exception:
            return Response({'error': 'Invalid refresh token'}, status=status.HTTP_401_UNAUTHORIZED)


# 🚪 Logout View
class LogoutView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh')
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception:
                pass

        response = Response({'message': 'Logged out'}, status=status.HTTP_200_OK)
        response.delete_cookie('access')
        response.delete_cookie('refresh')
        return response


# 🧾 Protected Dashboard View
class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': 'Welcome to your dashboard'})
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class LoginView(APIView):
    def get(self, request):
        return Response({'detail': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # Step 1: Look up user by email
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)

        # Step 2: Authenticate using username (Django default)
        user = authenticate(request, username=user_obj.username, password=password)
        if user is None:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)

        # Step 3: Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        # Step 4: Return response with httpOnly cookies
        response = Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        response.set_cookie('access', access_token, httponly=True, secure=True, samesite='Lax')
        response.set_cookie('refresh', refresh_token, httponly=True, secure=True, samesite='Lax')
        return response
