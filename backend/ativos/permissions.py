
from rest_framework.permissions import BasePermission


class SomenteUsuarioAutenticado(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
        )
