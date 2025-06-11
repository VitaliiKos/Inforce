from django.urls import path

from .views import RestaurantCreateView, RestaurantActionsView

urlpatterns = [
    path('', RestaurantCreateView.as_view(), name='restaurant_create'),
    path('<int:pk>', RestaurantActionsView.as_view(), name='restaurant-actions'),
]
