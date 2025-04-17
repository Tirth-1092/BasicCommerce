from rest_framework import permissions

class IsCartOwner(permissions.BasePermission):
    """
    Custom permission to allow only the cart owner to access or modify the cart.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
