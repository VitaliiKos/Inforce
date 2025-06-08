from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from apps.dishes.models import Dish
from apps.dishes.serializers import DishSerializer
from apps.restaurant.models import Restaurant
from utils.permissions.restaurant_permissions import IsRestaurantOwner


class DishListCreateView(ListCreateAPIView):
    serializer_class = DishSerializer
    permission_classes = [IsAuthenticated, IsRestaurantOwner]

    def get_queryset(self):
        return Dish.objects.filter(restaurant_id=self.kwargs.get('pk'))

    def perform_create(self, serializer):
        restaurant = Restaurant.objects.get(pk=self.kwargs.get('pk'))
        serializer.save(restaurant=restaurant)


class DishActionsView(RetrieveUpdateDestroyAPIView):
    queryset = Dish.objects.select_related('restaurant')
    serializer_class = DishSerializer
    permission_classes = [IsAuthenticated, IsRestaurantOwner]
