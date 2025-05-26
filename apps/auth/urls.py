from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import AuthMeView, AuthRegisterView, GoogleOAuthView, ActivateUserView

urlpatterns = [
    path('', TokenObtainPairView.as_view(), name='auth_login'),
    path('me', AuthMeView.as_view(), name='auth_me'),
    path('refresh', TokenRefreshView.as_view(), name='auth_refresh'),
    path('sign-up', AuthRegisterView.as_view(), name='auth_register'),
    path('oauth/google', GoogleOAuthView.as_view(), name='auth0_google'),
    path('verify-email/<str:token>', ActivateUserView.as_view(), name='auth_users_activate'),
]
