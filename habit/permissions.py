from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Ограничение для работы только с собственными привычками"""
    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner:
            return True
        return False
