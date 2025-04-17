from rest_framework import permissions

class IsPromotionAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff
