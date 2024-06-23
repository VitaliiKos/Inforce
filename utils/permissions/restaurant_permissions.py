from rest_framework import permissions

from apps.restaurant.models import Restaurant


class IsRestaurantOwner(permissions.BasePermission):
    """Custom permission to allow the restaurant owner to have full access.

    This permission class checks if the request user is the owner of the company.
    """

    def has_permission(self, request, view):
        restaurant_id = view.kwargs.get('pk')
        if not restaurant_id:
            return False

        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)
        except Restaurant.DoesNotExist:
            return False

        return restaurant.is_owner(request.user)
