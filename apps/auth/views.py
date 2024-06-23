from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny

from apps.employee.models import Employee
from apps.employee.serializers import EmployeeSerializer

UserModel: Employee = get_user_model()


class AuthRegisterView(CreateAPIView):
    serializer_class = EmployeeSerializer
    permission_classes = (AllowAny,)


class AuthMeView(RetrieveAPIView):
    serializer_class = EmployeeSerializer
    queryset = UserModel.objects.all()

    def get_object(self):
        return self.request.user
