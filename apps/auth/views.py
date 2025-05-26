from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView, RetrieveAPIView, GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from apps.employee.models import Employee
from apps.employee.serializers import EmployeeSerializer, GoogleOAuthSerializer
from utils.services.jwt_service import JWTService, ActivateToken

UserModel: Employee = get_user_model()


class AuthRegisterView(CreateAPIView):
    """
    Register User
    """
    serializer_class = EmployeeSerializer
    permission_classes = (AllowAny,)


class AuthMeView(RetrieveAPIView):
    """
    Return authorization user
    """
    serializer_class = EmployeeSerializer
    queryset = UserModel.objects.all()

    def get_object(self):
        return self.request.user


class GoogleOAuthView(CreateAPIView):
    """
    Register User with Google OAuth
    """
    serializer_class = GoogleOAuthSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": EmployeeSerializer(user).data
        }, status=status.HTTP_200_OK)


class ActivateUserView(GenericAPIView):
    """
    Activate User by token
    """
    permission_classes = (AllowAny,)

    @staticmethod
    def get(*args, **kwargs):
        token = kwargs['token']
        user = JWTService.validate_token(token, ActivateToken)
        user.is_active = True
        user.save()
        serializer = EmployeeSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
