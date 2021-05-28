from rest_framework import permissions

class IsUserOnly(permissions.BasePermission):
    """
    Permission to allow only user to change its slots.
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user