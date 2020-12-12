from rest_framework.permissions import BasePermission
from oauth2_provider.models import get_access_token_model


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        access_token = get_access_token_model()
        if request.user and request.user.is_authenticated:
            is_oauth = access_token.objects.filter(user__pk=request.user.pk, token=request.auth).exists()
            if not is_oauth:
                return True
            else:
                return False

    def has_object_permission(self, request, view, obj):
        access_token = get_access_token_model()
        if request.user and request.user.is_authenticated:
            owner = getattr(obj, "owner", None)
            if owner is None:
                return False
            else:
                is_oauth = access_token.objects.filter(user__pk=request.user.pk, token=request.auth).exists()
                if owner == request.user and not is_oauth:
                    return True
                else:
                    return False
