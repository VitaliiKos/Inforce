from rest_framework import serializers

from apps.employee.serializers import EmployeeSerializer
from apps.restaurant.models import Menu, Restaurant, Vote


class RestaurantSerializer(serializers.ModelSerializer):
    owner = EmployeeSerializer(read_only=True)

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'owner')


class MenuSerializer(serializers.ModelSerializer):
    restaurant = RestaurantSerializer(read_only=True)

    class Meta:
        model = Menu
        fields = ('id', 'date', 'dish', 'restaurant')


class VoteSerializer(serializers.ModelSerializer):
    menu = MenuSerializer(read_only=True)
    employee = EmployeeSerializer(read_only=True)

    class Meta:
        model = Vote
        fields = ('id', 'menu', 'employee')
