from rest_framework.permissions import BasePermission

class Permission_View(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated)