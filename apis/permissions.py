from rest_framework import permissions

class IsMasterOrReadOnly(permissions.BasePermission):
    """
    Разрешает создание и редактирование только мастерам.
    Просмотр разрешен всем аутентифицированным пользователям.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_master

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.master.user == request.user

class IsServiceOwner(permissions.BasePermission):
    """
    Разрешает редактирование услуги только её владельцу (мастеру).
    """
    def has_object_permission(self, request, view, obj):
        return obj.master.user == request.user

class CanChangeServiceStatus(permissions.BasePermission):
    """
    Проверяет возможность изменения статуса услуги в зависимости от текущего статуса.
    """
    def has_object_permission(self, request, view, obj):
        if not request.user.is_master or obj.master.user != request.user:
            return False

        # Получаем новый статус из запроса
        new_status = request.data.get('status')
        if not new_status:
            return True

        # Правила перехода статусов
        valid_transitions = {
            'DR': ['AC', 'CN'],  # Из черновика можно только активировать или отменить
            'AC': ['PA', 'CM', 'CN'],  # Из активного можно приостановить, завершить или отменить
            'PA': ['AC', 'CN'],  # Из приостановленного можно активировать или отменить
            'CM': [],  # Из завершенного нельзя никуда перейти
            'CN': []  # Из отмененного нельзя никуда перейти
        }

        return new_status in valid_transitions.get(obj.status, [])
