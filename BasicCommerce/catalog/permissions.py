from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only admins to create, update, or delete objects.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff

class IsSellerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only sellers to create, update, or delete products.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role == 'seller'

class IsReviewOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only the review owner to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user