from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=['get'], detail=False)
    def first_names(self, request):
        users_first_names = User.objects.values_list('first_name', flat=True)

        return Response({'first_names': users_first_names})

    @action(methods=['get'], detail=True)
    def first_name(self, request, pk=None):
        user = User.objects.get(id=pk)
        first_name = user.first_name

        return Response({'first_name': first_name})


"""
	Если стандартных маршрутов, сформированых роутером недостаточно, то можно определить свои. Для этого есть специальный
    декоратор, который называется @action.

    Прописывается он во ViewSet. Декоратор принимает 2 параметра. Это список методов methods и detail, параметр отвечающий
    за то, будет ли возвращаться список объектов или один объект. Если один, то к декорируемому методу нужно добавить
    параметр, отвечающий за идентификацию объекта(например pk)

    @action(methods=['get'], detail=False)
    def first_names(self, request):
        users_first_names = User.objects.values_list('first_name', flat=True)

        return Response({'first_names': users_first_names})
    
    Таким образом мы создаем свой кастомный экшен и сопоставляем его с типом запроса от клиента(в данном случае get).

    Роутер имея информацию о нашем ViewSet видет это и создает для нашего кастомного экшена новый маршрут.
    Имя декорированного метода(first_names) добавляется в новый, сформированный маршрут.

    Теперь у нас есть новый маршрут 'api/v1/users/first_names' и его словарь сопоставлений {'get': 'first_names'}

    <URLPattern '^users/first_names/$' [name='user-first-names']>,
    <URLPattern '^users/first_names\.(?P<format>[a-z0-9]+)/?$' [name='user-first-names']>


    Пример экшена возвращающего один объект, вместо списка:

    @action(methods=['get'], detail=True)
    def first_name(self, request, pk=None):
        user = User.objects.get(id=pk)
        first_name = user.first_name

        return Response({'first_name': first_name})

    Маршрут для такого экшена будет сформирован таким - 'api/v1/users/<pk>/first_name'. Вместо pk должно ставиться число.
    То есть идентификатор пользователю нужно прописывать перед названием экшена

    <URLPattern '^users/(?P<pk>[^/.]+)/first_name/$' [name='user-first-name']>,
    <URLPattern '^users/(?P<pk>[^/.]+)/first_name\.(?P<format>[a-z0-9]+)/?$' [name='user-first-name']>,
"""