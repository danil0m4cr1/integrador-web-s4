
from rest_framework.permissions import BasePermission, SAFE_METHODS


class SomenteAdminParaAlteracoes(BasePermission):

    def has_permission(self, request, view):

        # Consultas liberadas para todos
        if request.method in SAFE_METHODS:
            return True

        # Alterações permitidas somente para administradores
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_staff
        )
