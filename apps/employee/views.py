from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.employee.models import Employee

from .serializers import EmployeeSerializer

EmployeeModel: Employee = get_user_model()


class EmployeeListView(ListAPIView):
    """List of employees"""
    serializer_class = EmployeeSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = EmployeeModel.objects.exclude(pk=self.request.user.pk)
        return queryset
