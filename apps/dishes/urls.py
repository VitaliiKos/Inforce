from django.urls import path
from .views import DishListCreateView, DishActionsView

urlpatterns = [
    path('<int:pk>/dishes', DishListCreateView.as_view(), name='dish_list_create'),
    path('dishes/<int:pk>', DishActionsView.as_view(), name='dish-actions'),
]
