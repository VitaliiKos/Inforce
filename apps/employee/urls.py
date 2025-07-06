from django.urls import path
from .views import (
    EmployeeListView,
    EmployeeDetailView,
    UserProfileUpdateView,
    ChangePasswordView,
    DeleteMyAccountView,
)

urlpatterns = [
    path('', EmployeeListView.as_view(), name='employee_list'),
    path('<int:pk>/', EmployeeDetailView.as_view(), name='employee_detail'),
    path('me/profile', UserProfileUpdateView.as_view(), name='employee_profile_update'),
    path('me/change-password', ChangePasswordView.as_view(), name='employee_change_password'),
    path('me/delete', DeleteMyAccountView.as_view(), name='employee_delete'),
]
