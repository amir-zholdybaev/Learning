from rest_framework import generics
from rest_framework.permissions import AllowAny


class UserAPIList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


"""
	AllowAny - Полный доступ

	IsAuthenticated - Только для авторизованных пользователей

	IsAdminUser - Только для администраторов

	IsAuthenticatedOrReadOnly - Только для авторизованных или всем, но для чтения


	Можно создавать свои классы permissions.

	Все классы ограничения доступа наследуются от BasePermission
"""


class BasePermission(metaclass=BasePermissionMetaclass):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return True


"""
	У него есть 2 метода has_permission и has_object_permission.
	Первый метод has_permission отвечает за настройку прав доступа на уровне всего запроса от клиента
	Второй метод has_object_permission отвечает за настройку прав доступа на уровне отдельного объекта
"""


"""
	Здесь мы создали свой класс permission IsAdminOrReadOnly - Только для администратора или всем, но для чтения
"""


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(request.user and request.user.is_staff)

        # return bool(
        #     request.method in SAFE_METHODS or
        #     request.user and
        #     request.user.is_staff
        # )


"""
	Здесь мы создали свой класс permission IsOwnerOrReadOnly - Только для вледельца(например поста) или всем, но для чтения
	Сделали мы эту настройку на уровне отдельного объекта.
"""


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user


"""
	Чтобы настроить права доступа глобально, то нужно указать класс Permission в файле settings.py, в словаре
	REST_FRAMEWORK, в списке под ключом 'DEFAULT_PERMISSION_CLASSES'.
	Таким образом мы задаем поведение по умолчанию для все вьюх, но внутри конкретной вьюхи можно переопределить этот
	permission класс.
"""


RES_FRAMEWORK = {
	'DEFAULT_PERMISSION_CLASSES': [
		'rest_framework.permissions.IsAuthenticated',
	]
}
