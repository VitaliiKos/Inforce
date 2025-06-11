from django.urls import path

from apps.menu.views import CreateDailyMenuView, TodayMenuView, DailyMenuActionsView

urlpatterns = [
    path('create', CreateDailyMenuView.as_view(), name='create_menu'),
    path('today', TodayMenuView.as_view(), name='today_menu'),
    path('<int:pk>', DailyMenuActionsView.as_view(), name='menu-actions'),
]
