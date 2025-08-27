from django.urls import path
from .views import landing_page
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
from .views import LogoutView
# In urls.py
from django.urls import path
from .views import (
    LoginView,
    CustomTokenRefreshView,
    LogoutView,
    DashboardView,)

urlpatterns = [
    path('', landing_page, name='landing'),
    path('signup/', views.signup_view, name='signup'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('login/', views.login_view, name='Login'),
    # path('dashboard/', views.user_dashboard, name='userdashboard'),

    path('', landing_page, name='landing'),
    
    path('login/', views.LoginView.as_view(), name='login'),
    path('refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', DashboardView.as_view(), name='userdashboard'),
    path('auth/login/', LoginView.as_view(), name='login'),

    

    

]
