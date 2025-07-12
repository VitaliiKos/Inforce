from rest_framework import serializers

from apps.employee.serializers import EmployeeSerializer
from apps.restaurant.models import Restaurant


class RestaurantSerializer(serializers.ModelSerializer):
    owner = EmployeeSerializer(read_only=True)

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'owner', 'created_at', 'updated_at')
