from rest_framework import permissions


class IsRestaurantOwner(permissions.BasePermission):
    """Custom permission to allow the restaurant owner to have full access.

    This permission class checks if the request user is the owner of the restaurant.
    """

    def has_object_permission(self, request, view, obj):
        return obj.is_owner(request.user)
