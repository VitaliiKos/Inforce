from django.urls import path

from .views import CurrentDayMenuView, CurrentDayResultsView, MenuCreateView, RestaurantCreateView, VoteCreateView

urlpatterns = [
    path('', RestaurantCreateView.as_view(), name='restaurant_create'),
    path('<int:pk>/menus/', MenuCreateView.as_view(), name='menu_create'),
    path('menus/today', CurrentDayMenuView.as_view(), name='current_day_menu'),
    path('menu/<int:pk>/votes', VoteCreateView.as_view(), name='vote_create'),
    path('votes/today', CurrentDayResultsView.as_view(), name='current_day_results'),
]
