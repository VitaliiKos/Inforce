from datetime import date

from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated

from utils.permissions.restaurant_permissions import IsRestaurantOwner

from .models import Menu, Restaurant, Vote
from .serializers import MenuSerializer, RestaurantSerializer, VoteSerializer


class RestaurantCreateView(ListCreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MenuCreateView(CreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = (IsAuthenticated, IsRestaurantOwner)

    def perform_create(self, serializer):
        restaurant = get_object_or_404(Restaurant, pk=self.kwargs.get('pk'))
        serializer.save(restaurant=restaurant)


class CurrentDayMenuView(ListAPIView):
    serializer_class = MenuSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Menu.objects.filter(date=date.today())


class VoteCreateView(CreateAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        menu = get_object_or_404(Menu, pk=self.kwargs.get('pk'))
        serializer.save(menu=menu, employee=self.request.user)


class CurrentDayResultsView(ListAPIView):
    serializer_class = VoteSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Vote.objects.filter(menu__date=date.today())
