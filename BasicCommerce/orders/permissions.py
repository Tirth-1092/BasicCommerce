from rest_framework import permissions

class IsOrderOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class CanCancelOrder(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.status in ['pending', 'processing']
