from rest_framework.permissions import BasePermission


class IsUser(BasePermission):
    """User может просматривать и обновлять только свой профиль"""
    def has_object_permission(self, request, view, obj):
        if request.user.email == obj.email:
            return True
        return False
