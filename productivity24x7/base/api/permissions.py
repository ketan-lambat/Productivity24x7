from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_superuser:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_authenticated:
            owner = getattr(obj, "owner", None)
            if owner is None:
                return False
            else:
                if owner == request.user:
                    return True
                else:
                    return False
