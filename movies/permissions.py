from rest_framework import permissions


class IsAuthenticatedOrPostOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Se for uma requisição de leitura (GET, HEAD, OPTIONS) e o usuário estiver autenticado, permita.
        if request.method in permissions.SAFE_METHODS and request.user and request.user.is_authenticated:
            return True

