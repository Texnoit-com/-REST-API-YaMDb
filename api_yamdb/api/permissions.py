from rest_framework import permissions


class IsAdminOrForbidden(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True


class IsRoleAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated and user.is_admin
            or user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            user.is_authenticated and user.is_admin
            or user.is_superuser
        )


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin or request.user.is_superuser
        )
