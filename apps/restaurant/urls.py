from django.urls import path

from .views import RestaurantCreateView, RestaurantRetrieveUpdateDestroyView

urlpatterns = [
    path('', RestaurantCreateView.as_view(), name='restaurant_create'),
    path('<int:pk>', RestaurantRetrieveUpdateDestroyView.as_view(), name='restaurant-detail'),
]
