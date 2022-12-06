from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):  # этот класс создаем сами, используя наработки класса IsAdminOnly (bool)
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class IsOwnerOrReadOnly(permissions.BasePermission):  # этот класс часто используется, поэтому импортируем его из документацити
    def has_object_permission(self, request, view, obj):  # здесь мы делаем разрешение на уровне одной записи, одного объекта, в отличие от класса выше
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user