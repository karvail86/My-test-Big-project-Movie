from rest_framework import permissions


class UserStatusPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.status == 'pro':
            return True
        elif request.user.status == 'simple' and obj.status == 'simple':
            return True
        return False


class CreatePermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.status == 'pro'
