from rest_framework.generics import CreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated


from django.utils.timezone import now

from apps.menu.models import DailyMenu
from apps.menu.serializers import DailyMenuSerializer
from utils.permissions.isAdmin_permissions import IsAdminUser


class CreateDailyMenuView(CreateAPIView):
    queryset = DailyMenu.objects.all()
    serializer_class = DailyMenuSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class TodayMenuView(RetrieveAPIView):
    serializer_class = DailyMenuSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        today = now().date()
        return DailyMenu.objects.get(date=today)

class DailyMenuActionsView(RetrieveUpdateDestroyAPIView):
    queryset = DailyMenu.objects.all()
    serializer_class = DailyMenuSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]