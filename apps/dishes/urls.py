from django.urls import path

from apps.dishes.views import DishListCreateView, DishActionsView

urlpatterns = [
    path('restaurant/<int:pk>', DishListCreateView.as_view(), name='dish_list_create'),
    path('<int:pk>', DishActionsView.as_view(), name='dish-actions'),
]
