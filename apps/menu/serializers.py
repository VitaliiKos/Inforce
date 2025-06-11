from django.db import transaction
from rest_framework import serializers
from rest_framework.serializers import RelatedField

from apps.dishes.models import Dish
from apps.dishes.serializers import DishSerializer
from apps.menu.models import DailyMenu
from apps.restaurant.models import Restaurant


class RestaurantRelatedFieldSerializer(RelatedField):

    def to_representation(self, value: Restaurant):
        return {'id': value.id, 'name': value.name, 'owner_id': value.owner_id}


class DailyMenuSerializer(serializers.ModelSerializer):
    restaurant = RestaurantRelatedFieldSerializer(read_only=True)
    dishes = DishSerializer(many=True, read_only=True)
    dish_ids = serializers.PrimaryKeyRelatedField(queryset=Dish.objects.all(), many=True, write_only=True)

    class Meta:
        model = DailyMenu
        fields = ('id', 'restaurant', 'date', 'dishes', 'dish_ids', 'created_at', 'updated_at')
        read_only_fields = ('restaurant', 'created_at', 'updated_at')

    def validate_dish_ids(self, dishes):
        if not dishes:
            raise serializers.ValidationError("At least one dish must be selected.")

        restaurant = dishes[0].restaurant

        for dish in dishes:
            if dish.restaurant != restaurant:
                raise serializers.ValidationError("All dishes must belong to the same restaurant.")

        self.restaurant = restaurant
        return dishes

    @transaction.atomic
    def create(self, validated_data):
        dishes = list(set(validated_data.pop('dish_ids', [])))
        menu = DailyMenu.objects.create(date=validated_data['date'], restaurant=self.restaurant)
        menu.dishes.set(dishes)
        return menu

    @transaction.atomic
    def update(self, instance, validated_data):
        dishes = list(set(validated_data.pop('dish_ids', [])))
        if dishes is not None:
            instance.dishes.set(dishes)
        instance.save()
        return instance
